from MyCustomLLM.CustomLLM import my_llm
from utilities.util import extractIntegerFromLLMResponse
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)

age_template = """You are an AI assistant that extracts the numeric age from user input.
Output only the age as an integer, without any additional text.

User: {user_reply}

"""

prompt = PromptTemplate(template=age_template, input_variables=['user_reply'])

age_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)






def get_age_score():
    print("What is your age?")
    user_response = (input("    > "))
    parsedAge = extractIntegerFromLLMResponse(age_chain.run(user_response))
    print("Parsed age by AI: ", parsedAge)

    if parsedAge > 75 or parsedAge < 18:
                return 10
    elif 66 <= parsedAge <= 75:
                return 20
    elif 55 <= parsedAge <= 65:
                return 30
    elif 45 <= parsedAge <= 55:
                return 40
    elif 18 <= parsedAge <= 45:
                return 50
    
