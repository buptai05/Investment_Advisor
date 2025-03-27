from MyCustomLLM.CustomLLM import my_llm

from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)

invested_percentage_template = """
You are an AI assistant that extracts and returns only the numeric percentage value from the user's reply. Do not include any additional text or explanations in your response. If no percentage value is found, return "None".

User Reply: {user_reply}

Percentage:
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
            
            percentage = float(res)

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
    






