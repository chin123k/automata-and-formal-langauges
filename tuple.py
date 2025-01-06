from ply import lex
from ply import yacc

# List of token names
tokens = (
    'TYPE',
    'IDENTIFIER',
    'ASSIGN',
    'COMMA',
    'NUMBER',
    'STRING',
    'BOOLEAN',
    'NONE',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ASSIGN = r'='
t_COMMA = r','
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_TYPE(t):
    r'const|let|var'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
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

t_ignore = ' \t\n'  # Added newline to ignore

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
                 | declaration'''
    p[0] = "Valid"

def p_declaration(p):
    '''declaration : TYPE IDENTIFIER ASSIGN tuple'''

def p_tuple(p):
    '''tuple : LPAREN elements_opt RPAREN'''

def p_elements_opt(p):
    '''elements_opt : elements
                    | empty'''

def p_elements(p):
    '''elements : value
                | elements COMMA value'''

def p_value(p):
    '''value : NUMBER
             | STRING
             | BOOLEAN
             | NONE
             | tuple'''  # Support nested tuples
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token: {p.type}, value: {p.value}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

if __name__ == '__main__':
    while True:
        try:
            check = input("Press Y/N to Validate Syntax: ")
            if check.upper() != 'Y':
                break
            s = input('Enter Python code: ')
            if not s:
                continue
            result = parser.parse(s)
            print("Valid syntax\n" if result == "Valid" else "Invalid syntax\n")
        except EOFError:
            break
