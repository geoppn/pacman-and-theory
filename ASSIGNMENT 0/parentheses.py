
def complete_parentheses(expression):
    # INITIALIZE AN EMPTY LIST TO HOLD THE RESULT
    result = []
    # INITIALIZE A COUNTER TO KEEP TRACK OF THE NUMBER OF RIGHT PARENTHESES
    right_paren_count = 0
    max_streak = 0
    
    # FIRST PASS: COUNT THE NUMBER OF RIGHT PARENTHESIS AND BUILD THE INITIAL RESULT LIST
    for char in expression:
        if char == ')':
            right_paren_count += 1
            current_streak += 1 # GET THE MAXIMUM STREAK OF RIGHT PARENTHESIS, TO ENSURE SMOOTHER AND MORE LOGICAL PARENTHESIS INSERTION
            if current_streak > max_streak:
                max_streak = current_streak
        elif char != ' ': # IGNORE SPACES WHEN DEALING WITH THE STREAK COUNTER
            current_streak = 0
        result.append(char)
    
    # SECOND PASS: ITERATE THROUGH THE RESULT AND ADD LEFT PARENTHESIS
    i = 0
    while i < len(result):
        # FIND THE NEXT RIGHT PARENTHESIS
        while i < len(result) and result[i] != ')':
            i += 1
        # MOVE FORWARD UNTIL AFTER THE NEXT OPERATOR
        while i < len(result) and result[i] not in '+-*/':
            i += 1
        if i < len(result):
            if max_streak > 1: # IF THE MAXIMUM STREAK OF RIGHT PARENTHESIS IS GREATER THAN 1, ADD AN EXTRA LEFT PARENTHESIS TO PROMOTE MORE USEFUL PARENTHESIS
                result.insert(i + 1, '((')
                right_paren_count -= 2 # DISCARD TWO PARENTHESIS
                max_streak -= 2 # DECREASE THE STREAK
            else:
                result.insert(i + 1, '(')
                right_paren_count -= 1
        i += 1
    
    # ADD THE NECESSARY/REMAINING NUMBER OF LEFT PARENTHESIS AT THE BEGINNING
    result = ['('] * right_paren_count + result
    
    # JOIN THE LIST INTO A STRING AND REMOVE ALL SPACES
    return ''.join(result).replace(' ', '')

# EXAMPLE USAGE

user_input = input("Enter the expression: ")
# CONVERT THE INPUT STRING INTO A LIST
expression_list = list(user_input.replace(" ", ""))  # REMOVE SPACES AND CONVERT TO LIST (INPUT MUST BE A LIST, AS REQUESTED)

print(complete_parentheses(expression_list))