import time
import os

from dotenv import load_dotenv
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Request, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, select, text
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError, InternalError
from jwt.exceptions import InvalidTokenError
from security import *
from models import *
from uuid import uuid4
from db import engine, vector_engine
from automata import Automata
from state import State
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

load_dotenv()

automata = Automata("template-1")

docs_root = os.getenv('DOCS_ROOT')

allowed_content_types = [ 
    "application/pdf"
]

def is_valid_content_type(content_type):
    return content_type in allowed_content_types

def get_session():
    with Session(engine) as session:
        yield session
        
def get_vector_session():
    with Session(vector_engine) as session:
        yield session
        
def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.pwd):
        return False
    return user

def get_user(username: str):
    try:
        statement = select(User).where(User.username == username)
        with Session(engine) as session:
            res = session.exec(statement).one()
        return res
    except NoResultFound: 
        print("No result found")
    except MultipleResultsFound:
        print("Multiple results found")
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
    
SessionDep = Annotated[Session, Depends(get_session)]
VecSessionDep = Annotated[Session, Depends(get_vector_session)]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('FRONTEND_URL')],  # Modifica con il dominio del tuo frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()] 
) -> Token:
    
    user = authenticate_user(form_data.username, form_data.password) 
    if user == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    refresh_token = create_access_token({"sub": user.username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)

@app.post("/refresh-token")
async def refresh_access_token(request: RefreshToken):
    refresh_token = request.refresh_token
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_access_token({"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[UserBase, Depends(get_current_active_user)] 
):
    return current_user

@app.post("/users/create")
async def create_user(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    user: User, 
    session: SessionDep) -> User:
    try:
        user.pwd = get_password_hash(user.pwd)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists"
        )
         
@app.post("/documents/upload")
async def create_upload_file(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    file: Annotated[UploadFile, File()],
    session: SessionDep
):
    try:
        if is_valid_content_type(file.content_type):
            
            results = session.exec(select(Document).where(Document.filename == file.filename and Document.user_id == current_user.id)).all()
            
            if len(results) > 0:
                raise HTTPException(
                    status_code=status.HTTP_208_ALREADY_REPORTED, 
                    detail="A file with that name is already present"
                )
            
            hashed_name = f"{str(uuid4())}.pdf"
            collection_name = current_user.username
            
            file_location = f"{docs_root}/{hashed_name}"
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())
                                
            result = automata.save_document(hashed_name, collection_name)
            
            document = Document(
                filename=file.filename,
                extension=file.content_type,
                hashname=hashed_name,
                visible=True,
                user_id=current_user.id
            )
            
            session.add(document)
            session.commit()
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type"
            )
    except InternalError:
        os.remove(f"{docs_root}/{file.filename}")
        
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unknown error"
            )
        
@app.get("/collection/user_collections")
async def get_user_collection_info(
    vector_session: VecSessionDep,
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
):
    
    try:
        results = vector_session.exec(select(LangChainCollection).where(LangChainCollection.name == current_user.username)).one()
        
        return results
    except NoResultFound: 
        print("No result found")
    except MultipleResultsFound:
        print("Multiple results found")
        
@app.get("/documents/user_documents")
async def get_user_collection_info(
    session: SessionDep,
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
):
    
    results = session.exec(select(Document).where(Document.user_id == current_user.id)).all()
    return results

@app.post("/chat/question")
async def create_upload_file(
    session: SessionDep,
    chat_question : ChatQuestion,
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
):
    state = State({"question" : chat_question.question, "collection_name" : current_user.username})
    response = automata.invoke(state)
    
    chat_message = Chat(question=chat_question, answer=response['answer'], user_id=current_user.id)
    
    session.add(chat_message)
    session.commit()
    session.refresh(chat_message)
    
    return {
        "answer" : response['answer']
    }
    
@app.get("/documents/download/{document_id}")
async def download_document(
    document_id: int, 
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    session: SessionDep,
):
    
    document = session.exec(select(Document).where(Document.id == document_id)).one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Documento non trovato, record non presente")

    document_path = f"{docs_root}/{document.hashname}"

    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Documento non trovato, file non presente")
        

    return FileResponse(document_path, filename=os.path.basename(document_path), media_type="application/pdf")

@app.post("/chat/topics")
async def create_chat_topic(
    chatTopicCreate : ChatTopicCreate, 
    session: SessionDep, 
    current_user: UserBase = Depends(get_current_active_user)):
    
    name = chatTopicCreate.name

    topic_count = session.exec(select(ChatTopic).where(ChatTopic.user_id == current_user.id)).all()
    
    if len(topic_count) >= 10: 
        raise HTTPException(status_code=400, detail="Limite massimo di 10 chat raggiunto.")

    topic = ChatTopic(name=name, user_id=current_user.id)
    session.add(topic)
    session.commit()
    session.refresh(topic)
    
    return topic

@app.get("/chat/topics")
async def get_user_topics(
    session: SessionDep, 
    current_user: UserBase = Depends(get_current_active_user)
):
    topics = session.exec(select(ChatTopic).where(ChatTopic.user_id == current_user.id)).all()
    return topics

@app.get("/chat/topics/{idx}")
async def get_user_topics(
    idx : int,
    session: SessionDep, 
    current_user: UserBase = Depends(get_current_active_user)
):
    topic = session.exec(select(ChatTopic).where(ChatTopic.user_id == current_user.id and ChatTopic.id == idx)).one_or_none()
    return topic