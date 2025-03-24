import re

def extractIntegerFromLLMResponse(sentence):
    # Use regex to find all sequences of digits and filter threm as string
    integers = re.findall(r'\d+', sentence)
    integers = [int(num) for num in integers]
    return integers[-1]