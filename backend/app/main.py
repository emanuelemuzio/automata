from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import *
from .config import *
from .automata import * 
from .router.users import router as users_router
from .router.auth import router as auth_router
from .router.documents import router as document_router
from .router.chat import router as chat_router
from .router.chattopic import router as chat_topic_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(chat_topic_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],  
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
    openapi_data = app.openapi()

    with open("openapi.json", "w") as file:
        json.dump(openapi_data, file)