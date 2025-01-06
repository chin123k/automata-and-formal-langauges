from ply import lex
from ply import yacc

# List of token names
tokens = (
    'IDENTIFIER',
    'ASSIGN',
    'OPEN',
    'READ',
    'WRITE',
    'CLOSE',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'STRING',
    'SEMICOLON',
    'DOT',  # Add DOT token
)

# Regular expression rules for simple tokens
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'  # Define DOT token

# Keywords for file operations
def t_OPEN(t):
    r'open'
    return t

def t_READ(t):
    r'read'
    return t

def t_WRITE(t):
    r'write'
    return t

def t_CLOSE(t):
    r'close'
    return t

# Strings enclosed in double quotes
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove the surrounding quotes
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Parsing rules
def p_statement(p):
    '''statement : file_operation SEMICOLON
                 | file_operation'''  # Allow optional semicolon
    p[0] = "Valid"

def p_file_operation(p):
    '''file_operation : IDENTIFIER ASSIGN OPEN LPAREN STRING COMMA STRING RPAREN
                      | IDENTIFIER DOT READ LPAREN RPAREN
                      | IDENTIFIER DOT WRITE LPAREN STRING RPAREN
                      | IDENTIFIER DOT CLOSE LPAREN RPAREN'''
    p[0] = "Valid file operation"

def p_error(p):
    if p:
        print("Syntax error at token:", p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# Main function to prompt user input and validate it
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
        else:
            print("Invalid syntax\n")
