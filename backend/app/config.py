import json
import os

CURRENT_ENV = os.getenv("CURRENT_ENV", "local")

config_dict = None

with open("config.json", "r") as f:
    config_dict = json.load(f)[CURRENT_ENV] 
    
LLM_MODEL = config_dict['LLM_MODEL']
LLM_TEMPERATURE = int(config_dict['LLM_TEMPERATURE'])
LLM_TEMPLATE = config_dict['LLM_TEMPLATE']
DOCS_ROOT = config_dict['DOCS_ROOT']
PROMPT = config_dict['PROMPT']
LANGUAGE = config_dict['LANGUAGE']
MODEL_PROVIDER = config_dict['MODEL_PROVIDER']

POSTGRES_USER = config_dict['POSTGRES_USER']
POSTGRES_PASSWORD = config_dict['POSTGRES_PASSWORD']
POSTGRES_DB_PGV = config_dict['POSTGRES_DB_PGV']
POSTGRES_DB_PG = config_dict['POSTGRES_DB_PG']
POSTGRES_PORT = config_dict['POSTGRES_PORT']
POSTGRES_HOST = config_dict['POSTGRES_HOST']
CONNECTION_STRING = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_PGV}"
config_dict['CONNECTION_STRING'] = CONNECTION_STRING

SECRET_KEY = config_dict['SECRET_KEY']
ALGORITHM = config_dict['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(config_dict['ACCESS_TOKEN_EXPIRE_MINUTES'])

FRONTEND_URL = config_dict['FRONTEND_URL']
REFRESH_TOKEN_EXPIRE_DAYS = int(config_dict['REFRESH_TOKEN_EXPIRE_DAYS'])

allowed_origins = [
    "http://localhost:3000", 
    "http://frontend:3000",   
]

allowed_content_types = [ 
    "application/pdf"
] 