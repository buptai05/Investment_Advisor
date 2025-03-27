from MyCustomLLM.CustomLLM import my_llm
from utilities.util import extract_numeric_value
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)

# OLD TEMPLAE

# income_percentage_template = """
# You are an AI assistant that extracts and returns only the numeric percentage value from the user's reply. Do not include any additional text or explanations in your response. If no percentage value is found, return "None".

# User Reply: {user_reply}

# Percentage:
# """

income_percentage_template =  """
    You are a smart data extractor. 
    The user has been asked: 
    "What percentage of your annual household income could be available for investment or savings?"

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


prompt = PromptTemplate(template=income_percentage_template, input_variables=['user_reply'])

income_percentage_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)



def get_income_percentage_score():
    attempts = 0
    while True:
        try:
            print("\nWhat percentage of your annual household income could be available for investment or savings?")
            
            choice = input("    > ")
            # print(income_percentage_chain.run(choice))
            res = income_percentage_chain.run(choice)
            print("RESPONSE: ", res)
            # parsed_income_percentage = extractIntegerFromLLMResponse(income_percentage_chain.run(choice))
            
            # None--> ulta seedha jawab, non-contextual reply
            if "None" in res :
                raise ValueError("Invalid input. Please enter a number between 0 and 100.")
            
            #not none ----> contextual and numeric reply 
            elif  not 0 <= float( extract_numeric_value(res)) <= 100:
                raise ValueError("Invalid input. Please enter a number between 0 and 100.")
            
            parsed_income_percentage = float( extract_numeric_value(res))
            print("Parsed income percentage: ", parsed_income_percentage)

            if parsed_income_percentage ==0:
                return 10
            elif 0 < parsed_income_percentage <= 10:
                return 20
            elif 10 < parsed_income_percentage <= 25:
                return 30
            elif 25 < parsed_income_percentage <= 50:
                return 40
            elif 50< parsed_income_percentage:
                return 50
            
        except ValueError as e:
            print("\n" + str(e) + "\n")
            attempts += 1
            if attempts > 2:
                print("Valid input : any number B/W 0 to 100")

# DRIVER FUNCTION FOR TESTING STANDALONE MODULE
# COMMAND :- python -m AIQuestions.IncomePercentageQuestion
if __name__ == "__main__":
    get_income_percentage_score()
    






