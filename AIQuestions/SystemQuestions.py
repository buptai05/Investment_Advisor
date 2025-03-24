#ORIGINSL QURESTIONS WITHOUT AI FOR BACKUP

def get_age_score():
    attempts = 0
    while True:
        try:
            print("What is your age?")
            age = input("    > ")
            if not age.isdigit():
                raise ValueError("Please enter a valid age.")
            age = int(age)
            if age < 0 or age > 120:
                raise ValueError("Please enter an age between 0 and 120.")
            if age > 75 or age < 18:
                return 10
            elif 66 <= age <= 75:
                return 20
            elif 55 <= age <= 65:
                return 30
            elif 45 <= age <= 55:
                return 40
            elif 18 <= age <= 45:
                return 50
        except ValueError as e:
            print("\n" + str(e) + "\n")
            attempts += 1
            if attempts > 2:
                print("Valid input (example: 30, 100, 50, 85, 41)")
               
 
def get_stage_of_life_score():
    while True:
        try:
            print("\nWhich of the following best describes your current stage of life?")
            print("1. Few financial obligations, single or family, wanting to build wealth.")
            print("2. Many financial obligations, single or family, limited earnings/savings.")
            print("3. Married with financial commitments, financially stable now but uncertain about the future.")
            print("4. Mature family. In peak earning years, expenses under control, planning for retirement.")
            print("5. Close to retirement and major family financial obligations taken care of, seeking a comfortable future.")
            print("6. Retired, living on savings, investments, or pension.")
            choice = input("    > ")
            if not choice.isdigit() or not 1 <= int(choice) <= 6:
                raise ValueError("Invalid input. Please select a number between 1 and 6.")
            scores = [50, 30, 40, 50, 20, 10]
            return scores[int(choice) - 1]
        except ValueError as e:
            print("\n" + str(e) + "\n")
 
def get_income_percentage_score():
    attempts = 0
    while True:
        try:
            print("\nWhat percentage of your annual household income could be available for investment or savings?")
            print("1. 0%")
            print("2. Between >0% and 10%")
            print("3. Between >10% and 25%")
            print("4. Between >25% and 50%")
            print("5. Over 50%")
            choice = input("    > ")
            if not choice.isdigit() or not 1 <= int(choice) <= 5:
                raise ValueError("Invalid input. Please select a number between 1 and 5.")
            scores = [10, 20, 30, 40, 50]
            return scores[int(choice) - 1]
        except ValueError as e:
            print("\n" + str(e) + "\n")
            attempts += 1
            if attempts > 2:
                print("Valid input (example: 1, 2, 3, 4, 5)")
               
 
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
            if not choice.isdigit() or not 1 <= int(choice) <= 5:
                raise ValueError("Invalid input. Please select a number between 1 and 5.")
            scores = [10, 20, 30, 40, 50]
            return scores[int(choice) - 1]
        except ValueError as e:
            print("\n" + str(e) + "\n")
 
def get_risk_tolerance_score():
    while True:
        try:
            print("\nWhich statement best describes your investment objective and risk tolerance?")
            print("1. Very low risk taker. (I avoid any short-term fluctuations. Protecting my capital is my priority.)")
            print("2. Low risk taker. (I want returns just above savings interest. I avoid short-term fluctuations.)")
            print("3. Average risk taker. (I want to preserve my capital but accept minor short-term changes. I can take some risk for higher returns.)")
            print("4. High risk taker. (I prefer a balanced approach and can accept negative fluctuations for better returns.)")
            print("5. Very high-risk taker. (I seek the highest returns and can accept short-term losses.)")
            choice = input("    > ")
            if not choice.isdigit() or not 1 <= int(choice) <= 5:
                raise ValueError("Invalid input. Please select a number between 1 and 5.")
            scores = [10, 20, 30, 40, 50]
            return scores[int(choice) - 1]
        except ValueError as e:
            print("\n" + str(e) + "\n")
 
def get_investment_percentage_score():
    attempts = 0
    while True:
        try:
            print("\nApproximately what percentage of your assets (excluding own use property) is currently held in investment products where the value can fluctuate?")
            percentage = input("    > ")
            if not percentage.isdigit():
                raise ValueError("Please enter a valid percentage.")
            percentage = int(percentage)
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
            if attempts > 2:
                print("Valid input (example: 30, 100, 50, 85, 41)")
                print("Invalid input (example: 20.4, 45yrs, @30)\n")
 
def get_investment_duration_score():
    while True:
        try:
            print("\nFor how long would you expect most of your money to remain invested before you would need to access it?")
            print("1. < 1 year")
            print("2. 1 year - 3 years")
            print("3. 4-5 years")
            print("4. 6-9 years")
            print("5. 10 years and above")
            choice = input("    > ")
            if not choice.isdigit() or not 1 <= int(choice) <= 5:
                raise ValueError("Invalid input. Please select a number between 1 and 5.")
            scores = [10, 20, 30, 40, 50]
            return scores[int(choice) - 1]
        except ValueError as e:
            print("\n" + str(e) + "\n")
 
def get_unforeseen_events_score():
    while True:
        try:
            print("\nHow many months of expenses have you put aside to meet unforeseen events?")
            print("1. Have no amount set aside for unforeseen events")
            print("2. Less than 3 months")
            print("3. Between 3 months and <6 months")
            print("4. Between 6 months and <9 months")
            print("5. Over 9 months")
            choice = input("    > ")
            if not choice.isdigit() or not 1 <= int(choice) <= 5:
                raise ValueError("Invalid input. Please select a number between 1 and 5.")
            scores = [10, 20, 30, 40, 50]
            return scores[int(choice) - 1]
        except ValueError as e:
            print("\n" + str(e) + "\n")