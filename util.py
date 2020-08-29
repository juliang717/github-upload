def is_number(inp_str):
    '''
    Returns True if the input string is a floating point number or an integer, and False otherwise.
    '''
    pre_digit = 0
    dot = 0
    post_digit = 0

    for char in inp_str:
        if char == '.':
            dot += 1
        elif char.isdigit():
            if dot == 0:
                pre_digit += 1
            else:
                post_digit += 1
        else:
            return False
    
    if (pre_digit < 1) or (dot > 1) or (dot == 1 and post_digit == 0):
        return False
    
    return True

def get_key_by_value(input_dict, value):
    for item in input_dict.items():
        if item[1] == value:
            return item[0]
    return None