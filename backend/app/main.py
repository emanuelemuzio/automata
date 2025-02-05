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
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[UserBase, Depends(get_current_active_user)] 
):
    return current_user

@app.post("/users/")
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
         
@app.post("/upload_document")
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
        
@app.get("/collection/get_user_collection")
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
        
@app.get("/documents/get_user_documents")
async def get_user_collection_info(
    session: SessionDep,
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
):
    
    results = session.exec(select(Document).where(Document.user_id == current_user.id)).all()
    return results

@app.post("/chat/question")
async def create_upload_file(
    chat_question : ChatQuestion,
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
):
    state = State({"question" : chat_question.question, "collection_name" : current_user.username})
    response = automata.invoke(state)
    
    return {
        "answer" : response['answer']
    }