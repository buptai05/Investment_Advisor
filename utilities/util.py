import re

def extractIntegerFromLLMResponse(sentence):
    # Use regex to find all sequences of digits and filter threm as string
    integers = re.findall(r'\d+', sentence)
    integers = [int(num) for num in integers]
    return integers[-1]




def parse_numeric_pair(input_string):
    # Find all (A,B) patterns in the string
    matches = re.findall(r'\(([^)]+)\)', input_string)
    
    for match in matches:
        try:
            # Split by comma and strip whitespace
            a, b = map(str.strip, match.split(','))
            
            # Convert to float (handles both int and float for A)
            a_float = float(a)
            b_float = float(b)  # Will convert integer strings properly
            
            return a_float, b_float
            
        except (ValueError, AttributeError):
            continue
    
    return None, None  # Return None if no valid pair found

