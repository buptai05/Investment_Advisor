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






def get_stage_of_life_score():
    while True:
        try:
            print("\nWhich of the following best describes your current stage of life? Please select a number between 1 and 6")
            print("1. Few financial obligations, single or family, wanting to build wealth.")
            print("2. Many financial obligations, single or family, limited earnings/savings.")
            print("3. Married with financial commitments, financially stable now but uncertain about the future.")
            print("4. Mature family. In peak earning years, expenses under control, planning for retirement.")
            print("5. Close to retirement and major family financial obligations taken care of, seeking a comfortable future.")
            print("6. Retired, living on savings, investments, or pension.")
            choice = input("    > ")
            # print(option_chain.run(choice))
            parsed_choice_in_digit = extractIntegerFromLLMResponse(option_chain.run(choice))
            print("Parsed choice by AI: ", parsed_choice_in_digit)

            if not 1 <= parsed_choice_in_digit <= 6:
                raise ValueError("Invalid input. Please select a number between 1 and 6.")
            scores = [50, 30, 40, 50, 20, 10]
            return scores[parsed_choice_in_digit - 1]
        except ValueError as e:
            print("\n" + str(e) + "\n")
    
