from AIQuestions import SystemQuestions, AgeQuestion, StageOfLifeQuestion, IncomePercentageQuestion, FinancialKnowledgeQuestion, InvestedAssetPercentageQuestion ,RiskToleranceQuestion, InvestmentDurationQuestion, UnforeseenEventsDurationQuestion

def calculate_investor_profile(total_score):
    if total_score <= 100:
        return "Conservative", "You are a Conservative investor. Risk must be very low, and you are prepared to accept lower returns to protect capital. Your primary objective is to protect wealth."
    elif 101 <= total_score <= 180:
        return "Cautious", "You are a Cautious investor seeking better than basic returns, but risk must be low. You want to protect your wealth, and you are prepared to consider less aggressive growth investments."
    elif 181 <= total_score <= 260:
        return "Growth", "You are a Prudent investor who wants a balanced portfolio to work towards medium to long term financial goals. You believe in taking calculated risks to achieve good returns."
    elif 261 <= total_score <= 350:
        return "Assertive", "You are an Assertive investor, probably earning sufficient income to invest most funds for capital growth. You are prepared to accept higher volatility and moderate risks. Your primary concern is to accumulate assets over the medium to long term. You require a balanced portfolio, but more aggressive investments may be included to meet your goal."
    elif 351 <= total_score <= 400:
        return "Aggressive", "You are an Aggressive investor. Your primary investment objective is to grow your wealth. To achieve great long-term returns - you can accept negative fluctuations on your portfolio in the short term. Your investment choices are diverse, but carry with them a higher level of risk. You believe in taking great risk for greater rewards."
 
def runScript():
    total_score = 0
    

    total_score += AgeQuestion.get_age_score()
    total_score += StageOfLifeQuestion.get_stage_of_life_score()
    total_score += IncomePercentageQuestion.get_income_percentage_score()
    total_score += FinancialKnowledgeQuestion.get_financial_knowledge_score()
    total_score += RiskToleranceQuestion.get_risk_tolerance_score()
    total_score += InvestedAssetPercentageQuestion.get_investment_percentage_score()
    total_score += InvestmentDurationQuestion.get_investment_duration_score()
    total_score += UnforeseenEventsDurationQuestion.get_unforeseen_events_score()
 
    profile, description = calculate_investor_profile(total_score)
    print(f"\nInvestor Profile: {profile} ({total_score})")
    print("Know more")
    input("Press Enter to see the detailed description...\n")
    print(description)
 


runScript()