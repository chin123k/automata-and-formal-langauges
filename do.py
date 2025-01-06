from ply import lex
from ply import yacc

# Tokens
tokens = (
    'WHILE', 'DEF', 'CLASS', 'IF', 'ELIF', 'ELSE', 'FOR', 'IN', 'RETURN', 'PASS',
    'IDENTIFIER', 'NUMBER', 'STRING', 'ASSIGN', 'LOGICAL', 'COMPARISON',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COLON',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'POWER',
    'NONE', 'BOOLEAN', 'COMMA', 'DOT',
)

# Precedence rules to resolve shift/reduce conflicts
precedence = (
    ('left', 'LOGICAL'),
    ('left', 'COMPARISON'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),  # Unary minus
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

# Ignore whitespace and comments
t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

# Handle newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Keywords
keywords = {
    'while': 'WHILE',
    'def': 'DEF',
    'class': 'CLASS',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'for': 'FOR',
    'in': 'IN',
    'return': 'RETURN',
    'pass': 'PASS',
    'True': 'BOOLEAN',
    'False': 'BOOLEAN',
    'None': 'NONE',
    'and': 'LOGICAL',
    'or': 'LOGICAL',
    'not': 'LOGICAL'
}

def t_NUMBER(t):
    r'\d*\.\d+|\d+'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Create lexer
lexer = lex.lex()

# Parser rules
def p_program(p):
    '''program : statements'''
    p[0] = {'type': 'program', 'body': p[1]}

def p_statements(p):
    '''statements : statement
                 | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : simple_stmt
                | compound_stmt'''
    p[0] = p[1]

def p_simple_stmt(p):
    '''simple_stmt : small_stmt'''
    p[0] = p[1]

def p_small_stmt(p):
    '''small_stmt : expr_stmt
                 | return_stmt
                 | pass_stmt'''
    p[0] = p[1]

def p_expr_stmt(p):
    '''expr_stmt : assignment
                | expr'''
    p[0] = p[1]

def p_compound_stmt(p):
    '''compound_stmt : if_stmt
                    | while_stmt
                    | for_stmt
                    | function_def
                    | class_def'''
    p[0] = p[1]

def p_if_stmt(p):
    '''if_stmt : IF test COLON suite
               | IF test COLON suite else_block'''
    if len(p) == 5:
        p[0] = {'type': 'if', 'test': p[2], 'body': p[4]}
    else:
        p[0] = {'type': 'if', 'test': p[2], 'body': p[4], 'else': p[5]}

def p_else_block(p):
    '''else_block : ELSE COLON suite
                 | ELIF test COLON suite
                 | ELIF test COLON suite else_block'''
    if len(p) == 4:
        p[0] = {'type': 'else', 'body': p[3]}
    elif len(p) == 5:
        p[0] = {'type': 'elif', 'test': p[2], 'body': p[4]}
    else:
        p[0] = {'type': 'elif', 'test': p[2], 'body': p[4], 'else': p[5]}

def p_while_stmt(p):
    '''while_stmt : WHILE test COLON suite'''
    p[0] = {'type': 'while', 'test': p[2], 'body': p[4]}

def p_for_stmt(p):
    '''for_stmt : FOR IDENTIFIER IN expr COLON suite'''
    p[0] = {'type': 'for', 'target': p[2], 'iter': p[4], 'body': p[6]}

def p_function_def(p):
    '''function_def : DEF IDENTIFIER LPAREN parameter_list RPAREN COLON suite'''
    p[0] = {'type': 'function', 'name': p[2], 'params': p[4], 'body': p[7]}

def p_class_def(p):
    '''class_def : CLASS IDENTIFIER COLON suite
                | CLASS IDENTIFIER LPAREN parameter_list RPAREN COLON suite'''
    if len(p) == 5:
        p[0] = {'type': 'class', 'name': p[2], 'body': p[4]}
    else:
        p[0] = {'type': 'class', 'name': p[2], 'bases': p[4], 'body': p[7]}

def p_suite(p):
    '''suite : simple_stmt
            | LBRACE statements RBRACE'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[2]

def p_parameter_list(p):
    '''parameter_list : parameters
                     | empty'''
    p[0] = p[1] if p[1] else []

def p_parameters(p):
    '''parameters : IDENTIFIER
                 | parameters COMMA IDENTIFIER'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_test(p):
    '''test : expr
            | expr COMPARISON expr
            | expr LOGICAL expr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'type': 'operation', 'op': p[2], 'left': p[1], 'right': p[3]}

def p_expr(p):
    '''expr : term
            | expr PLUS term
            | expr MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'type': 'operation', 'op': p[2], 'left': p[1], 'right': p[3]}

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor
            | term MODULO factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'type': 'operation', 'op': p[2], 'left': p[1], 'right': p[3]}

def p_factor(p):
    '''factor : PLUS factor
              | MINUS factor %prec UMINUS
              | power'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'type': 'unary', 'op': p[1], 'operand': p[2]}

def p_power(p):
    '''power : atom
             | atom POWER factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'type': 'operation', 'op': p[2], 'left': p[1], 'right': p[3]}

def p_atom(p):
    '''atom : IDENTIFIER
            | NUMBER
            | STRING
            | BOOLEAN
            | NONE
            | LPAREN expr RPAREN
            | atom DOT IDENTIFIER'''
    if len(p) == 2:
        p[0] = {'type': 'atom', 'value': p[1]}
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = {'type': 'attribute', 'object': p[1], 'attr': p[3]}

def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expr'''
    p[0] = {'type': 'assign', 'target': p[1], 'value': p[3]}

def p_return_stmt(p):
    '''return_stmt : RETURN
                  | RETURN expr'''
    if len(p) == 2:
        p[0] = {'type': 'return', 'value': None}
    else:
        p[0] = {'type': 'return', 'value': p[2]}

def p_pass_stmt(p):
    '''pass_stmt : PASS'''
    p[0] = {'type': 'pass'}

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Create parser
parser = yacc.yacc()

def validate_python(code):
    """Validate Python code and return the AST if valid"""
    try:
        ast = parser.parse(code)
        return True, ast
    except Exception as e:
        return False, str(e)

def main():
    while True:
        try:
            print("\nOptions:")
            print("1. Validate Python code")
            print("2. Exit")
            choice = input("Enter choice (1-2): ")
            
            if choice == '1':
                code = input('Enter Python code: ')
                if not code:
                    continue
                
                is_valid, result = validate_python(code)
                if is_valid:
                    print("Valid Python syntax!")
                    print("AST:", result)
                else:
                    print("Invalid Python syntax!")
                    print("Error:", result)
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()