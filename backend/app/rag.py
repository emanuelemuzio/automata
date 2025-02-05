from langchain import hub
from dotenv import load_dotenv
from template import templates
from langchain_core.prompts import PromptTemplate
import os

load_dotenv()

RAG_PROMPT = os.getenv('RAG_PROMPT')

def hub_pull():
    prompt = hub.pull(RAG_PROMPT)
    return prompt
        
def get_wrapper(template_name="template-1"):
    template = templates[template_name]
    
    return PromptTemplate.from_template(template)