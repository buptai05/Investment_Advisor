from MyCustomLLM.CustomLLM import my_llm
from utilities.util import extractIntegerFromLLMResponse
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings
warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)

selected_user_option_template = """You are an AI assistant that parses and extracts the option number from user given input.
Output only the option number as an integer, without any additional text.

User: {user_reply}

"""

prompt = PromptTemplate(template=selected_user_option_template, input_variables=['user_reply'])

option_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)






def get_financial_knowledge_score():
    while True:
        try:
            print("\nHow familiar are you with financial markets and investment products?")
            print("1. No experience.")
            print("2. Basic knowledge.")
            print("3. Understand market fluctuations and sector wise differences in income, growth, and taxes.")
            print("4. Understand the importance of diversification.")
            print("5. Experienced.")
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
# COMMAND :- python -m AIQuestions.4A_FinancialKnowledgeQuestion
if __name__ == "__main__":
    get_financial_knowledge_score()