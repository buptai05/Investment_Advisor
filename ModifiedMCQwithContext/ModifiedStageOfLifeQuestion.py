from MyCustomLLM.CustomLLM import my_llm
from utilities.util import extractIntegerFromLLMResponse
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)

stage_Of_Life_template =  """
    You are an AI assistant designed to analyze user responses and match them to predefined life stages.

**Task:**
- The user will input a free-text response describing their current stage of life.
- Your job is to interpret their response, extract the underlying meaning, and match it with the most relevant predefined category.
- Respond ONLY with the corresponding number:
  - 50 → If the response matches: "Few financial obligations, single or family, wanting to build wealth."
  - 30 → If the response matches: "Many financial obligations, single or family, limited earnings/savings."
  - 40 → If the response matches: "Married with financial commitments, financially stable now but uncertain about the future."
  - 50 → If the response matches: "Mature family. In peak earning years, expenses under control, planning for retirement."
  - 20 → If the response matches: "Close to retirement and major family financial obligations taken care of, seeking a comfortable future."
  - 10 → If the response matches: "Retired, living on savings, investments, or pension."
  - none → If the response does not fit any of these categories or is irrelevant.

**Example Inputs and Outputs:**
- Input: "I'm young and just started working, no major responsibilities yet."
  - Output: 50
- Input: "I have a lot of bills and a family to take care of, but my income is not great."
  - Output: 30
- Input: "I'm married, have a home loan, financially doing okay but unsure about long-term security."
  - Output: 40
- Input: "We are financially stable, kids are growing, and I am focusing on retirement planning."
  - Output: 50
- Input: "I'm about to retire, no major expenses left, just want a secure future."  OR  "I am at the end of my career / service life"
  - Output: 20
- Input: "I'm retired and living off my pension and savings."
  - Output: 10
- Input: "I love pizza and traveling."
  - Output: none

**Instructions:**
- Do not return any extra text, explanations, or symbols—only the designated number or "none".
- Analyze responses for context rather than exact wording to determine the best match.


 User Reply:
"{user_reply}"

  Output:
  """

prompt = PromptTemplate(template=stage_Of_Life_template, input_variables=['user_reply'])

stage_Of_Life_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)






def get_stage_of_life_score():
    while True:
        
        print("\nWhich of the following best describes your current stage of life? Please select a number between 1 and 6")
        print("1. Few financial obligations, single or family, wanting to build wealth.")
        print("2. Many financial obligations, single or family, limited earnings/savings.")
        print("3. Married with financial commitments, financially stable now but uncertain about the future.")
        print("4. Mature family. In peak earning years, expenses under control, planning for retirement.")
        print("5. Close to retirement and major family financial obligations taken care of, seeking a comfortable future.")
        print("6. Retired, living on savings, investments, or pension.")
        choice = input("    > ")
            
        ans = stage_Of_Life_chain({'user_reply': choice})


        print("ANS : ", ans)   

# DRIVER FUNCTION FOR TESTING STANDALONE MODULE
# COMMAND :- python -m ModifiedMCQwithContext.ModifiedStageOfLifeQuestion
if __name__ == "__main__":
    get_stage_of_life_score()
    
