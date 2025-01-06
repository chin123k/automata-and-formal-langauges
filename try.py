from ply import lex
from ply import yacc

# List of token names
tokens = (
    'DEF', 'IDENTIFIER', 'NUMBER', 'STRING', 'ASSIGN', 'WHILE', 'LPAREN', 'RPAREN', 
    'LBRACE', 'RBRACE', 'PRINT', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'NULL', 
    'BOOLEAN', 'COMMA', 'SEMICOLON'
)

# Regular expressions for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_COMMA = r','
t_SEMICOLON = r';'

# More complex tokens
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Check for reserved words
    if t.value == 'def':
        t.type = 'DEF'
    elif t.value == 'while':
        t.type = 'WHILE'
    elif t.value == 'print':
        t.type = 'PRINT'
    elif t.value in ('true', 'false'):
        t.type = 'BOOLEAN'
    elif t.value == 'null':
        t.type = 'NULL'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Ignored characters (spaces, tabs, newlines)
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
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                 | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = p[1] + [p[2]] if p[2] is not None else p[1]

def p_statement(p):
    '''statement : function_decl
                | while_stmt
                | assign_stmt
                | print_stmt'''
    p[0] = p[1]

def p_function_decl(p):
    '''function_decl : DEF IDENTIFIER LPAREN param_list RPAREN LBRACE statements RBRACE'''
    p[0] = ('function_decl', p[2], p[4], p[7])

def p_param_list(p):
    '''param_list : IDENTIFIER
                 | param_list COMMA IDENTIFIER
                 | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]

def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN expression RPAREN LBRACE statements RBRACE'''
    p[0] = ('while_stmt', p[3], p[6])

def p_assign_stmt(p):
    '''assign_stmt : IDENTIFIER ASSIGN expression SEMICOLON'''
    p[0] = ('assign_stmt', p[1], p[3])

def p_print_stmt(p):
    '''print_stmt : PRINT LPAREN expression_list RPAREN SEMICOLON'''
    p[0] = ('print_stmt', p[3])

def p_expression_list(p):
    '''expression_list : expression
                      | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression(p):
    '''expression : term
                 | expression PLUS term
                 | expression MINUS term
                 | expression TIMES term
                 | expression DIVIDE term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary_op', p[2], p[1], p[3])

def p_term(p):
    '''term : IDENTIFIER
            | NUMBER
            | STRING
            | BOOLEAN
            | NULL
            | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = ('term', p[1])
    else:
        p[0] = p[2]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token: {p.value}")
    else:
        print("Syntax error at EOF")

# Build the parser with error recovery
parser = yacc.yacc()

# Interactive loop for input
if __name__ == '__main__':
    while True:
        try:
            check = input("Press Y/N to Validate Syntax: ")
            if check.lower() == 'n':
                break
            elif check.lower() == 'y':
                s = input('Enter Python-like code: ')
                if not s:
                    continue
                try:
                    result = parser.parse(s)
                    if result is not None:
                        print("Valid syntax")
                except:
                    print("Invalid syntax")
        except EOFError:
            break