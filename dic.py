import re
from ply import lex
from ply import yacc
import ast  # To safely evaluate input dictionary from user

# List of token names
tokens = (
    'TYPE',
    'IDENTIFIER',
    'ASSIGN',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'NUMBER',
    'STRING',
    'BOOLEAN',
    'NONE',  # Using 'NONE' for Python's 'None'
    'SEMICOLON',
)

# Regular expression rules for simple tokens
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ASSIGN = r'='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'

def t_TYPE(t):
    r'const|let|var'
    return t

def t_NUMBER(t):
    r'\d+\.\d+|\d+'  # Matches both float and integer numbers
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.value = t.value == 'true'
    return t

def t_NONE(t):
    r'None'
    t.value = None
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Define precedence and associativity
precedence = (
    ('left', 'COMMA'),
)

# Parsing rules
def p_statement(p):
    '''statement : declaration SEMICOLON
                 | declaration'''  # Allow the semicolon to be optional
    p[0] = "Valid"

def p_declaration(p):
    '''declaration : TYPE IDENTIFIER ASSIGN array'''

def p_array(p):
    '''array : LBRACKET elements_opt RBRACKET'''

def p_elements_opt(p):
    '''elements_opt : elements
                    | elements COMMA
                    | empty'''

def p_elements(p):
    '''elements : value
                | elements COMMA value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_value(p):
    '''value : NUMBER
             | STRING
             | BOOLEAN
             | NONE
             | array'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at token:", p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# Validation function for dictionary input
def validate_dict(data):
    # Check if data is a dictionary
    if not isinstance(data, dict):
        return "Invalid: Input is not a dictionary"

    # Check for required keys
    required_keys = {'type', 'identifier', 'value'}
    if not required_keys.issubset(data.keys()):
        return "Invalid: Missing required keys"

    # Validate 'type'
    if data['type'] not in {'const', 'let', 'var'}:
        return "Invalid: 'type' must be one of 'const', 'let', or 'var'"

    # Validate 'identifier' (must match identifier rules)
    if not isinstance(data['identifier'], str) or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', data['identifier']):
        return "Invalid: 'identifier' must be a valid identifier string"

    # Validate 'value' - recursive check for allowed data types
    if not validate_value(data['value']):
        return "Invalid: 'value' contains unsupported elements"

    return "Valid syntax"

def validate_value(value):
    # Check if value is a basic allowed type
    if isinstance(value, (int, float, str, bool)) or value is None:
        return True
    # Check if value is a list (array) and recursively validate each element
    elif isinstance(value, list):
        return all(validate_value(element) for element in value)
    else:
        return False

# Main function to prompt user input and validate it
if __name__ == '__main__':
    while True:
        user_input = input("Enter a dictionary to validate (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        try:
            # Safely parse user input as a dictionary
            test_data = ast.literal_eval(user_input)
            if isinstance(test_data, dict):
                print(validate_dict(test_data))
            else:
                print("Invalid input: Please enter a valid dictionary.")
        except (SyntaxError, ValueError):
            print("Invalid input: Please enter a valid dictionary format.")
