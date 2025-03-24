#Worked in Google Colab
# from langchain import HuggingFaceHub, PromptTemplate, LLMChain
from langchain_huggingface import HuggingFaceEndpoint

#Works in local, the above import wont work in local due to some library version upgrades
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
import os


# Option 1: Retrieve the API key directly from the environment
load_dotenv()
api_key = os.getenv("MY_SECRET_API_KEY")




model_id = 'mistralai/Mistral-Nemo-Instruct-2407'

# THIS ALSO WORKS BUT DEPRECATED
# my_llm = HuggingFaceHub(huggingfacehub_api_token=api_key,
#                             repo_id=model_id,
#                             model_kwargs={"temperature":0.8,"max_new_tokens":2000})

my_llm = HuggingFaceEndpoint(
    repo_id=model_id,
    task="text-generation",
    huggingfacehub_api_token=api_key,
    temperature=0.2,        
    max_new_tokens=20, 

)
