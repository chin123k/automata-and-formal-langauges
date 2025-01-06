from ply import lex
from ply import yacc

# List of token names
tokens = (
    'DEF', 'IDENTIFIER', 'NUMBER', 'STRING', 'ASSIGN', 'WHILE', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'PRINT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'NULL', 'BOOLEAN', 'COMMA'
)

# Regular expressions for tokens
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_COMMA = r','

# Reserved words
def t_DEF(t):
    r'def'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_BOOLEAN(t):
    r'true|false'
    return t

def t_NULL(t):
    r'null'
    return t

# Ignored characters
t_ignore = ' \t\n'

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
def p_program(p):
    '''program : statements'''
    pass

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    pass

def p_statement(p):
    '''statement : function_decl
                 | while_stmt
                 | assign_stmt
                 | print_stmt
                 | empty'''
    pass

def p_function_decl(p):
    '''function_decl : DEF IDENTIFIER LPAREN params RPAREN LBRACKET statements RBRACKET'''
    pass

def p_params(p):
    '''params : IDENTIFIER
              | IDENTIFIER COMMA params
              | empty'''
    pass

def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN expression RPAREN LBRACKET statements RBRACKET'''
    pass

def p_assign_stmt(p):
    '''assign_stmt : IDENTIFIER ASSIGN expression'''
    pass

def p_print_stmt(p):
    '''print_stmt : PRINT LPAREN expression RPAREN'''
    pass

def p_expression(p):
    '''expression : term
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    pass

def p_term(p):
    '''term : IDENTIFIER
            | NUMBER
            | STRING
            | BOOLEAN
            | NULL
            | LPAREN expression RPAREN'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at token:", p.value)
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Interactive loop for input
if __name__ == '__main__':
    while True:
        try:
            check = input("Press Y/N to Validate Syntax: ")
            if check.lower() == 'n':
                exit(0)
            elif check.lower() == 'y':
                s = input('Enter Python-like code: ')
                if not s:
                    continue
                result = parser.parse(s)
                if result is None:
                    print("Valid syntax")
                else:
                    print("Invalid syntax")
        except EOFError:
            break
