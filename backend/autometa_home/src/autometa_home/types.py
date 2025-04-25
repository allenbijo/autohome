from typeguard import check_type
from typing import List, Tuple
import re


def validate_result_format_tasks(result):
    try:
        # First try the original evaluation
        return True, check_type(eval(result.raw), List[Tuple[str, str, str]])
    except Exception:
        try:
            # Extract valid tokens using regex
            # Match words containing a-z, 0-9, hyphens and spaces
            tokens = re.findall(r'[a-zA-Z0-9-]+(?:\s+[a-zA-Z0-9-]+)*', result.raw)

            # Remove any empty strings
            tokens = [token.strip() for token in tokens if token.strip()]
            # Check if number of tokens is multiple of 3
            if len(tokens) % 3 != 0:
                raise ValueError("Number of tokens must be a multiple of 3")

            # Convert tokens into list of tuples
            formatted_result = []
            for i in range(0, len(tokens), 3):
                formatted_result.append((tokens[i], tokens[i + 1], tokens[i + 2]))

            return True, str(formatted_result)

        except Exception as e:
            return False, "FORMAT MUST BE LIST[ TUPLE[ STR, STR, STR ] ]"


def validate_result_format_devices(result):
    try:
        # First try the original evaluation
        return True, check_type(eval(result.raw), List[str])
    except Exception:
        try:
            # Extract valid tokens using regex
            # Match words containing a-z, 0-9, hyphens and spaces
            tokens = re.findall(r'[a-zA-Z0-9-]+', result.raw)

            # Remove any empty strings
            tokens = [token.strip() for token in tokens if token.strip()]

            return True, str(tokens)

        except Exception as e:
            return False, "FORMAT MUST BE LIST[ TUPLE[ STR, STR, STR ] ]"
        
        
def validate_result_format_new_state(text):
    try:
        return True, check_type(eval(text), List)
    except Exception:
        try:
            # Extract content inside square brackets
            tokens = re.findall(r'\[([\s\S]*?)\]', text.raw)

            return True, f"[{str(tokens.pop())}]"
        except Exception as e:
            return False, "FORMAT MUST BE LIST[ DICT ]"
