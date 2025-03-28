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

age_template = """You are an AI assistant that reads the user input for age and  parses whatever the number(integer/float) is just in front of years and months and returns it as a pair in the format (X,Y) where the input was X year Y month. If no unit is mentioned then assume it is in years.
If the input is only in years or 'Y' or 'y' or without any unit and the number is in float (for eg. "my age is M.N years" or "my age is M.N" ) then only return as (M.N,0) .If it the input age is only in momths (for eg. Y Months) then return the output in form of (0,Y) . Output only in this format, without any additional text.
For any non -contextual answers or answers which has not any link with age, return only None.
User: {user_reply}

"""

prompt = PromptTemplate(template=age_template, input_variables=['user_reply'])

age_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)





    

def get_investment_duration_score():
    while True:
        try:
            print("\nFor how long would you expect most of your money to remain invested before you would need to access it?")
            duration_input = input("    > ")

            res = age_chain.run(duration_input)
            print("RES: ", res)

            

            # match = re.match(r'(\d+(\.\d+)?)\s*(years?|y|months?|m)?', duration_input)
            # if not match:
            #     raise ValueError("Please enter a valid duration.")
           
            # duration_value, duration_unit = match.groups()[0], match.groups()[2]
            # duration_value = float(duration_value)
            # if duration_unit in ['months', 'month', 'm']:
            #     duration_value = duration_value / 12  # Convert months to years

            if "None" in res :
                raise ValueError("Invalid input. Please enter a number between 0 and 100.")
            

            Y, M = parse_numeric_pair(res)
            print(f"years: {Y}, months: {M}")

            duration_in_years = Y + M/12.0

            print("Derived duration: ", duration_in_years)
           
            if duration_in_years < 0:
                raise ValueError("Please enter a positive duration.")
            if duration_in_years < 1:
                return 10
            elif 1 <= duration_in_years < 3:
                return 20
            elif 3 <= duration_in_years < 5:
                return 30
            elif 5 <= duration_in_years < 10:
                return 40
            elif duration_in_years >= 10:
                return 50
        except ValueError as e:
            print("\n" + str(e) + "\n")            

# DRIVER FUNCTION FOR TESTING STANDALONE MODULE
# COMMAND :- python -m AIQuestions.InvestmentDurationQuestion
if __name__ == "__main__":
    get_investment_duration_score()
    
