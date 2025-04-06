from MyCustomLLM.CustomLLM import my_llm
from utilities.util import extractIntegerFromLLMResponse
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings

# Suppress Hugging Face deprecation warnings
warnings.simplefilter("ignore", FutureWarning)
warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)

financial_knowledge__template =  """
   You are an AI assistant designed to evaluate a user's familiarity with financial markets and investment products based on their free-text input.  

**Task:**  
- Analyze the user’s response.
- Determine which of the following five predefined categories best matches the context and intent of the input.
- Respond with ONLY the appropriate number listed below, or "none" if no category is relevant.

**Categories and Responses:**  
- 10 → No experience with financial markets or investment products.  
- 20 → Basic knowledge of financial terms or investing concepts.  
- 30 → Understands market fluctuations and how different sectors vary in income, growth, and taxation.  
- 40 → Understands the importance of diversification across investments.  
- 50 → Has hands-on experience with investing and financial markets.  
- none → Input is unrelated or non-contextual.

**Instructions:**  
- Do not return explanations, text, or symbols—only the number or "none".  
- Understand the user’s intent and financial literacy level, even if the wording is indirect.  
- Prioritize the *most fitting category* based on context, even if multiple seem close.

**Examples:**  
- Input: "I’ve never really looked into investing." → Output: 10  
- Input: "I know what stocks and mutual funds are but haven’t invested yet." → Output: 20  
- Input: "I check the market trends and know which sectors are performing well." → Output: 30  
- Input: "I believe in diversifying between equity, debt, and gold." → Output: 40  
- Input: "I've been investing for years in various asset classes." → Output: 50  
- Input: "I like coffee and long walks on the beach." → Output: none  

 
 User Reply:
"{user_reply}"

  Output:
  """

prompt = PromptTemplate(template=financial_knowledge__template, input_variables=['user_reply'])

financial_knowledge_chain=LLMChain(prompt=prompt, llm=my_llm, verbose=False)






def get_financial_knowledge_score():
    while True:
        
        print("\nHow familiar are you with financial markets and investment products?")
        print("1. No experience.")
        print("2. Basic knowledge.")
        print("3. Understand market fluctuations and sector wise differences in income, growth, and taxes.")
        print("4. Understand the importance of diversification.")
        print("5. Experienced.")
        user_input = input("    > ")
            
        ans = financial_knowledge_chain({'user_reply':user_input}) 

        print("ANS :", ans)
   

# DRIVER FUNCTION FOR TESTING STANDALONE MODULE
# COMMAND :- python -m AIQuestions.4B_FinancialKnowledgeQuestion
if __name__ == "__main__":
    get_financial_knowledge_score()
    
