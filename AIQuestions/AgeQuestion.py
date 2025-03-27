from MyCustomLLM.CustomLLM import my_llm
from utilities.util import extractIntegerFromLLMResponse, parse_numeric_pair
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)

# OLD TEMPLATE: WORKS FINE WITH ONLY INTEGER INPUT IN YEARS OR NO UNIT MENTIONED
# age_template = """You are an AI assistant that extracts the numeric age from user input.
# Output only the age as an integer, without any additional text.

# User: {user_reply}

# """
#farheen

age_template = """You are an AI assistant that reads the user input for age and  parses whatever the number(integer/float) is just in front of years and months and returns it as a pair in the format (X,Y) where the input was X year Y month. If no unit is mentioned then assume it is in years.
If the input is only in years or 'Y' or 'y' or without any unit and the number is in float (for eg. "my age is M.N years" or "my age is M.N" ) then only return as (M.N,0) .If it the input age is only in momths (for eg. Y Months) then return the output in form of (0,Y) . Output only in this format, without any additional text.

User: {user_reply}

"""

prompt = PromptTemplate(template=age_template, input_variables=['user_reply'])

age_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)




# OLD FUNCTION

# def get_age_score():
#     print("What is your age?")
#     user_response = (input("    > "))
#     parsedAge = extractIntegerFromLLMResponse(age_chain.run(user_response))
#     print("Parsed age by AI: ", parsedAge)

#     if parsedAge > 75 or parsedAge < 18:
#                 return 10
#     elif 66 <= parsedAge <= 75:
#                 return 20
#     elif 55 <= parsedAge <= 65:
#                 return 30
#     elif 45 <= parsedAge <= 55:
#                 return 40
#     elif 18 <= parsedAge <= 45:
#                 return 50




    

def get_age_score():
    attempts = 0
    while True:
        try:
            print("What is your age?")
            user_response = input("    > ")

            res = age_chain.run(user_response)
            print("RES: ", res)

            Y, M = parse_numeric_pair(res)
            print(f"years: {Y}, months: {M}")

            age_in_years = Y + M/12.0

            print("Derived age: ", age_in_years)
            
           
            if age_in_years < 0 or age_in_years > 120:
                raise ValueError("Please enter an age between 0 and 120.")
           
            if age_in_years > 75 or age_in_years < 18:
                return 10
            elif 66 <= age_in_years <= 75:
                return 20
            elif 55 <= age_in_years <= 65:
                return 30
            elif 45 <= age_in_years <= 55:
                return 40
            elif 18 <= age_in_years <= 45:
                return 50
        except ValueError as e:
            print("\n" + str(e) + "\n")
            attempts += 1
            # if attempts > 2:
            #     print("Valid input (example: 30, 100, 50, 85, 41)")
            

# DRIVER FUNCTION FOR TESTING STANDALONE MODULE
# COMMAND :- python -m AIQuestions.AgeQuestion
if __name__ == "__main__":
    get_age_score()
    
