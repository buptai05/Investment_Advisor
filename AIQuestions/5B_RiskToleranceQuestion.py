from MyCustomLLM.CustomLLM import my_llm
from utilities.util import extractIntegerFromLLMResponse
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)

template =  """
   You are an AI assistant tasked with understanding a user's investment objective and risk tolerance based on their open-ended response.

**Your Task:**
- Analyze the user’s input.
- Identify which of the five predefined categories best matches the context.
- Respond with **only** the appropriate numeric code (no text, explanation, or punctuation).
- If the input is unrelated or doesn’t fit any category, return **none**.

**Predefined Categories:**
- 10 → Very low risk taker: Wants no short-term fluctuations, prioritizes capital protection.
- 20 → Low risk taker: Wants slightly better than savings returns, avoids short-term volatility.
- 30 → Average risk taker: Aims to preserve capital, accepts some short-term change for returns.
- 40 → High risk taker: Balanced approach, accepts negative fluctuation for better returns.
- 50 → Very high risk taker: Seeks highest returns, accepts short-term losses.
- none → If input is non-contextual or irrelevant.

**Instructions:**
- Do not include any text, symbols, or descriptions—**only output the correct number or 'none'**.
- Understand the *intent and attitude toward risk* from the input, even if not explicitly stated.
- Choose the **most appropriate category** based on the input's tone, context, and meaning.

**Examples:**
- Input: "I prefer stability over high returns. I don’t want to lose my money." → Output: 10  
- Input: "I’m okay with a bit of market movement but want mostly safe options." → Output: 20  
- Input: "I can tolerate small risks if it means better returns in the long run." → Output: 30  
- Input: "I aim for higher returns and can take a few hits along the way." → Output: 40  
- Input: "I'm all in for maximum growth—even if the market crashes short term." → Output: 50  
- Input: "I love watching cricket and reading novels." → Output: none

 User Reply:
"{user_reply}"

  Output:
  """

prompt = PromptTemplate(template=template, input_variables=['user_reply'])

risk_taking__chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)






def get_risk_tolerance_score():
    while True:
        
        print("\nWhich statement best describes your investment objective and risk tolerance?")
        print("1. Very low risk taker. (I avoid any short-term fluctuations. Protecting my capital is my priority.)")
        print("2. Low risk taker. (I want returns just above savings interest. I avoid short-term fluctuations.)")
        print("3. Average risk taker. (I want to preserve my capital but accept minor short-term changes. I can take some risk for higher returns.)")
        print("4. High risk taker. (I prefer a balanced approach and can accept negative fluctuations for better returns.)")
        print("5. Very high-risk taker. (I seek the highest returns and can accept short-term losses.)")
        
        user_input = input("    > ")

        ans = risk_taking__chain({'user_reply':user_input}) 

        print("ANS ", ans)    

            


# DRIVER FUNCTION FOR TESTING STANDALONE MODULE
# COMMAND :- python -m AIQuestions.5B_RiskToleranceQuestion
if __name__ == "__main__":
    get_risk_tolerance_score()
    
