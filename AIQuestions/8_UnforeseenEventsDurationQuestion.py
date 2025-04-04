from MyCustomLLM.CustomLLM import my_llm
from utilities.util import parse_numeric_pair
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)

# OLD TEMPLATE: WORKS FINE WITH ONLY INTEGER INPUT IN YEARS OR NO UNIT MENTIONED
# age_template = """You are an AI assistant that extracts the numeric age from user input.
# Output only the age as an integer, without any additional text.

# User: {user_reply}

# """

time_duration_template = """You are an AI assistant that reads the user input for time duration and  parses whatever the number(integer/float) is just in front of years and months and returns it as a pair in the format (X,Y) where the input was X year Y month. If no unit is mentioned then assume it is in years.
If the input is only in years or 'Y' or 'y' or without any unit and the number is in float (for eg. "my age is M.N years" or "my age is M.N" ) then only return as (M.N,0) .If it the input age is only in momths (for eg. Y Months) then return the output in form of (0,Y) . Output only in this format, without any additional text.
For any non -contextual answers or answers which has not any link with age, return only None.
User: {user_reply}

"""

prompt = PromptTemplate(template=time_duration_template, input_variables=['user_reply'])

time_duration_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)



def get_unforeseen_events_score():
    while True:
        try:
            print("\nHow many months of expenses have you put aside to meet unforeseen events?")
            user_input = input("    > ")

            res = time_duration_chain.run(user_input)
            
            if "None" in res :
                raise ValueError("Please enter a valid number of months.")
           
            Y, M = parse_numeric_pair(res)
            print(f"years: {Y}, months: {M}")

            duration_in_years = Y + M/12.0

            print("Derived duration: ", duration_in_years)
            
            if duration_in_years < 0:
                raise ValueError("Please enter a positive number of months.")
            if duration_in_years == 0:
                return 10
            elif duration_in_years < 0.25:
                return 20
            elif 0.25 <= duration_in_years < 0.5:
                return 30
            elif 0.5 <= duration_in_years < 0.75:
                return 40
            elif duration_in_years >= 0.75:
                return 50
        except ValueError as e:
            print("\n" + str(e) + "\n")

# DRIVER FUNCTION FOR TESTING STANDALONE MODULE
# COMMAND :- python -m AIQuestions.UnforeseenEventsDurationQuestion
if __name__ == "__main__":
    get_unforeseen_events_score()
    
