#Worked in Google Colab
# from langchain import HuggingFaceHub, PromptTemplate, LLMChain

from dotenv import load_dotenv
#Works in local, the above import wont work in local due to some library version upgrades
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub

import re
import os

# Option 1: Retrieve the API key directly from the environment
load_dotenv()
api_key = os.getenv("MY_SECRET_API_KEY")
print("KEY:" ,api_key)

def extract_integers(sentence):
    # Use regex to find all sequences of digits and filter threm as string
    integers = re.findall(r'\d+', sentence)
    
    integers = [int(num) for num in integers]
    

    return integers[-1]

# model_id = 'tiiuae/falcon-7b-instruct'

model_id = 'mistralai/Mistral-Nemo-Instruct-2407'

my_llm = HuggingFaceHub(huggingfacehub_api_token=api_key,
                            repo_id=model_id,
                            model_kwargs={"temperature":0.8,"max_new_tokens":2000})
# template = """

# You are an AI assistant that receives user age via user given prompts and parses and extracts the age from it. You need to print only the age in integer in the next line.

# {user_reply}

# """

#  Strict Prompt to ensure only the number is returned
template = """You are an AI assistant that extracts the numeric age from user input.
Output only the age as an integer, without any additional text.

User: {user_reply}

"""

prompt = PromptTemplate(template=template, input_variables=['user_reply'])

age_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)

print(age_chain.run("I am of 56 "))

print(extract_integers(age_chain.run("My age is twelve currently")))

