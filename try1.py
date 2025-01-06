from ply import lex
from ply import yacc

# Tokens
tokens = (
    'WHILE', 'DEF', 'CLASS', 'IF', 'ELIF', 'ELSE', 'FOR', 'IN', 'RETURN', 'PASS',
    'IDENTIFIER', 'NUMBER', 'STRING', 'ASSIGN', 'LOGICAL', 'COMPARISON',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COLON',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'POWER',
    'NONE', 'BOOLEAN', 'COMMA', 'DOT',
    'SEMICOLON',  # Add SEMICOLON here
)

# Token definitions
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_POWER = r'\*\*'
t_COMMA = r','
t_DOT = r'\.'
t_COLON = r':'
t_COMPARISON = r'==|!=|<=|>=|<|>'
t_SEMICOLON = r';'  # Define semicolon token

t_ignore = ' \t\n'  # Ignore spaces, tabs, and newlines

def t_WHILE(t): r'while'; return t
def t_DEF(t): r'def'; return t
def t_CLASS(t): r'class'; return t
def t_IF(t): r'if'; return t
def t_ELIF(t): r'elif'; return t
def t_ELSE(t): r'else'; return t
def t_FOR(t): r'for'; return t
def t_IN(t): r'in'; return t
def t_RETURN(t): r'return'; return t
def t_PASS(t): r'pass'; return t
def t_BOOLEAN(t): r'True|False'; return t
def t_NONE(t): r'None'; return t
def t_LOGICAL(t): r'and|or|not'; return t

def t_NUMBER(t):
    r'\d*\.\d+|\d+'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Create lexer
lexer = lex.lex()

# Parser rules
def p_program(p):
    '''program : statements'''
    p[0] = 'Valid'

def p_statements(p):
    '''statements : statement
                 | statement statements'''

def p_statement(p):
    '''statement : simple_stmt
                | compound_stmt'''

def p_simple_stmt(p):
    '''simple_stmt : assignment
                  | expr
                  | return_statement
                  | pass_statement'''

def p_compound_stmt(p):
    '''compound_stmt : if_stmt
                    | while_stmt
                    | for_stmt
                    | function_def
                    | class_def'''

def p_if_stmt(p):
    '''if_stmt : IF comparison_expr COLON suite
               | IF comparison_expr COLON suite elif_stmts
               | IF comparison_expr COLON suite ELSE COLON suite'''

def p_elif_stmts(p):
    '''elif_stmts : ELIF comparison_expr COLON suite
                  | ELIF comparison_expr COLON suite elif_stmts'''

def p_while_stmt(p):
    '''while_stmt : WHILE comparison_expr COLON suite'''

def p_for_stmt(p):
    '''for_stmt : FOR IDENTIFIER IN expr COLON suite'''

def p_function_def(p):
    '''function_def : DEF IDENTIFIER LPAREN parameters RPAREN COLON suite'''

def p_class_def(p):
    '''class_def : CLASS IDENTIFIER COLON suite
                | CLASS IDENTIFIER LPAREN parameters RPAREN COLON suite'''

def p_suite(p):
    '''suite : simple_stmt
            | LBRACE statements RBRACE'''

def p_parameters(p):
    '''parameters : IDENTIFIER
                 | IDENTIFIER COMMA parameters
                 | empty'''

def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expr'''

def p_comparison_expr(p):
    '''comparison_expr : expr COMPARISON expr
                      | expr'''

def p_expr(p):
    '''expr : term
            | expr PLUS term
            | expr MINUS term'''

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor
            | term MODULO factor'''

def p_factor(p):
    '''factor : PLUS factor
              | MINUS factor
              | power'''

def p_power(p):
    '''power : atom
             | atom POWER factor'''

def p_atom(p):
    '''atom : IDENTIFIER
            | NUMBER
            | STRING
            | BOOLEAN
            | NONE
            | LPAREN expr RPAREN'''

def p_return_statement(p):
    '''return_statement : RETURN
                       | RETURN expr'''

def p_pass_statement(p):
    '''pass_statement : PASS'''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token: {p.value}")
    else:
        print("Syntax error at EOF")

# Create parser
parser = yacc.yacc()

# Main loop
def main():
    while True:
        try:
            check = input("Press Y/N to Validate Syntax: ")
            if check.upper() == 'N':
                break
            s = input('Enter Python code: ')
            if not s:
                continue
            
            # Check for semicolon at the end of statements
            if s.strip().endswith(';') and ':' not in s:
                print("Invalid Python syntax: semicolon not allowed here")
                continue
            
            result = parser.parse(s)
            if result == "Valid":
                print("Valid Python syntax")
            else:   
                print("Invalid Python syntax")
        except EOFError:
            break

if __name__ == "__main__":
    main()
