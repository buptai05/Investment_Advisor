from MyCustomLLM.CustomLLM import my_llm
from utilities.util import extractIntegerFromLLMResponse
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)

selected_user_option_template = """You are an AI assistant that parses and extracts the option number from user given input.
Output only the option number as an integer, without any additional text.

User: {user_reply}

"""

prompt = PromptTemplate(template=selected_user_option_template, input_variables=['user_reply'])

option_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)






def get_risk_tolerance_score():
    while True:
        try:
            print("\nWhich statement best describes your investment objective and risk tolerance?")
            print("1. Very low risk taker. (I avoid any short-term fluctuations. Protecting my capital is my priority.)")
            print("2. Low risk taker. (I want returns just above savings interest. I avoid short-term fluctuations.)")
            print("3. Average risk taker. (I want to preserve my capital but accept minor short-term changes. I can take some risk for higher returns.)")
            print("4. High risk taker. (I prefer a balanced approach and can accept negative fluctuations for better returns.)")
            print("5. Very high-risk taker. (I seek the highest returns and can accept short-term losses.)")
            print("Please provide the option number (1-5).")
            choice = input("    > ")

            

            parsed_choice_in_digit = extractIntegerFromLLMResponse(option_chain.run(choice))
            print("Parsed choice by AI: ", parsed_choice_in_digit)

            if  not 1 <= parsed_choice_in_digit <= 5:
                raise ValueError("Invalid input. Please select a number between 1 and 5.")
            
            scores = [10, 20, 30, 40, 50]
            return scores[parsed_choice_in_digit - 1]
        except ValueError as e:
            print("\n" + str(e) + "\n")


# DRIVER FUNCTION FOR TESTING STANDALONE MODULE
# COMMAND :- python -m AIQuestions.RiskToleranceQuestion
if __name__ == "__main__":
    get_risk_tolerance_score()
    
