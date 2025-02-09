import json
import os

CURRENT_ENV = os.getenv("CURRENT_ENV", "local")

config = None

with open("config.json", "r") as f:
    config = json.load(f)[CURRENT_ENV]
    
LLM_MODEL = config['LLM_MODEL']
LLM_TEMPERATURE = config['LLM_TEMPERATURE']
LLM_TEMPLATE = config['LLM_TEMPLATE']
DOCS_ROOT = config['DOCS_ROOT']
RAG_PROMPT = config['RAG_PROMPT']

POSTGRES_USER = config['POSTGRES_USER']
POSTGRES_PASSWORD = config['POSTGRES_PASSWORD']
POSTGRES_DB_PGV = config['POSTGRES_DB_PGV']
POSTGRES_DB_PG = config['POSTGRES_DB_PG']
POSTGRES_PORT = config['POSTGRES_PORT']
POSTGRES_HOST = config['POSTGRES_HOST']

SECRET_KEY = config['SECRET_KEY']
ALGORITHM = config['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['ACCESS_TOKEN_EXPIRE_MINUTES']

FRONTEND_URL = config['FRONTEND_URL']
REFRESH_TOKEN_EXPIRE_DAYS = config['REFRESH_TOKEN_EXPIRE_DAYS']

allowed_origins = [
    "http://localhost:3000", 
    "http://frontend:3000",   
]

del(config)