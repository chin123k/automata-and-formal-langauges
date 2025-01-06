from ply import lex
from ply import yacc

# List of token names
tokens = (
    'LAMBDA',
    'IDENTIFIER',
    'COLON',
    'NUMBER',
    'PLUS',
    'COMMA',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_COLON = r':'
t_PLUS = r'\+'
t_COMMA = r','
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Match identifiers
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value == 'lambda':
        t.type = 'LAMBDA'
    return t

# Match numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore whitespace and tabs
t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                     | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : lambda_expression SEMICOLON
                | lambda_expression'''
    p[0] = p[1]

def p_lambda_expression(p):
    '''lambda_expression : LAMBDA parameters COLON expression'''
    p[0] = {
        'type': 'lambda',
        'parameters': p[2],
        'body': p[4]
    }

def p_parameters(p):
    '''parameters : IDENTIFIER
                 | parameters COMMA IDENTIFIER
                 | empty'''
    if len(p) == 2:
        if p[1] is None:  # empty case
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression(p):
    '''expression : term
                 | expression PLUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {
            'type': 'binary_op',
            'op': '+',
            'left': p[1],
            'right': p[3]
        }

def p_term(p):
    '''term : factor
            | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_factor(p):
    '''factor : IDENTIFIER
              | NUMBER'''
    p[0] = {
        'type': 'identifier' if isinstance(p[1], str) else 'number',
        'value': p[1]
    }

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

def validate_lambda(code):
    """
    Validates lambda expression syntax and returns the parsed AST if valid
    """
    try:
        result = parser.parse(code)
        return True, result
    except Exception as e:
        return False, str(e)

if __name__ == '__main__':
    while True:
        try:
            check = input("Press Y/N to Validate Syntax (Y/N): ").upper()
            if check == 'N':
                break
            elif check == 'Y':
                code = input('Enter lambda expression: ')
                is_valid, result = validate_lambda(code)
                if is_valid:
                    print("Valid syntax!")
                    print("Parsed structure:", result)
                else:
                    print("Invalid syntax!")
                    print("Error:", result)
            else:
                print("Please enter Y or N")
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
