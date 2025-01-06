from ply import lex
from ply import yacc

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
    t.value = float(t.value) if '.' in t.value else int(t.value)  # Convert to appropriate numeric type
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove the surrounding quotes
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.value = t.value == 'true'  # Convert to boolean
    return t

def t_NONE(t):
    r'None'  # Python's None
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
    # You can add more actions here if needed

def p_array(p):
    '''array : LBRACKET elements_opt RBRACKET'''
    # You can add more actions here if needed

def p_elements_opt(p):
    '''elements_opt : elements
                    | elements COMMA
                    | empty'''  # Allow an optional ending comma

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

if __name__ == '__main__':
    while True:
        try:
            check = input("Press Y/N to Validate Syntax: ")
            if check == 'N':
                exit(0)
            else:
                s = input('Enter Python code: ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        if result == "Valid":
            print("Valid syntax\n")
