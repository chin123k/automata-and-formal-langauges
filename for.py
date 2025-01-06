from ply import lex
from ply import yacc

# Tokens
tokens = (
    'FOR', 'IN', 'IDENTIFIER', 'NUMBER', 'LPAREN', 'RPAREN', 'COLON', 'COMMA', 'RANGE'
)

# Token definitions
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_COMMA = r','

t_ignore = ' \t\n'

def t_FOR(t): r'for'; return t
def t_IN(t): r'in'; return t
def t_RANGE(t): r'range'; return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Create lexer
lexer = lex.lex()

# Parser rules

def p_for_loop(p):
    '''for_loop : FOR IDENTIFIER IN range_expr COLON'''
    p[0] = 'Valid for loop'

def p_range_expr(p):
    '''range_expr : RANGE LPAREN NUMBER RPAREN
                  | RANGE LPAREN NUMBER COMMA NUMBER RPAREN
                  | RANGE LPAREN NUMBER COMMA NUMBER COMMA NUMBER RPAREN'''
    
def p_error(p):
    if p:
        print(f"Syntax error at token: {p.value}")
    else:
        print("Syntax error at EOF")

# Create parser
parser = yacc.yacc()

# Main loop for user input
def main():
    while True:
        try:
            check = input("Press Y/N to Validate Syntax: ")
            if check.upper() == 'N':
                break
            s = input('Enter for loop code: ')
            if not s:
                continue
            result = parser.parse(s)
            if result == "Valid for loop":
                print("Valid for loop syntax")
            else:
                print("Invalid for loop syntax")
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
