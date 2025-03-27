from MyCustomLLM.CustomLLM import my_llm
from utilities.util import extract_numeric_value
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)

# OLD TEMPLATE
# invested_percentage_template = """
# You are an AI assistant that extracts and returns only the numeric percentage value from the user's reply. Do not include any additional text or explanations in your response. If no percentage value is found, return "None".

# User Reply: {user_reply}

# Percentage:
# """


invested_percentage_template =  """
    You are a smart data extractor. 
    The user has been asked: 
    "Approximately what percentage of your assets (excluding own use property) is currently held in investment products where the value can fluctuate?"

    The user may respond with a percentage value like: 5%, 20.23%, 34%, etc.
    Your task is to:
    1. Extract only the numeric percentage value (as a string). Ignore the '%' sign.
    2. If the user reply is irrelevant, unclear, or non-contextual (does not contain a valid number), return None.

    **Examples:**
    - User Reply: "About 35%" → Output: 35
    - User Reply: "Roughly 12.5 percent" → Output: 12.5
    - User Reply: "I don't know" → Output: None
    - User Reply: "Maybe stocks and mutual funds" → Output: None

    User Reply:
    "{user_reply}"

    Output:
    """

prompt = PromptTemplate(template=invested_percentage_template, input_variables=['user_reply'])

income_percentage_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)



def get_investment_percentage_score():
    attempts = 0
    while True:
        try:
            print("\nApproximately what percentage of your assets (excluding own use property) is currently held in investment products where the value can fluctuate?")
            user_input = input("    > ")

            
            res = income_percentage_chain.run(user_input)
            print("RESPONSE: ", res)
            
            if "None" in res :
                raise ValueError("Invalid input. Please enter a number between 0 and 100.")
            
            percentage = float( extract_numeric_value(res))

            if percentage < 0 or percentage > 100:
                raise ValueError("Please enter a percentage between 0 and 100.")
            if percentage == 0:
                return 10
            elif 0 < percentage <= 10:
                return 20
            elif 10 < percentage <= 25:
                return 30
            elif 25 < percentage <= 50:
                return 40
            elif percentage > 50:
                return 50
        except ValueError as e:
            print("\n" + str(e) + "\n")
            attempts += 1
            


# DRIVER FUNCTION FOR TESTING STANDALONE MODULE
# COMMAND :- python -m AIQuestions.InvestedAssetPercentageQuestion
if __name__ == "__main__":
    get_investment_percentage_score()
    






