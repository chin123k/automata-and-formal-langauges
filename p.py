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
    'NUMBER',  # Added for read/write size
    'MODE',    # Added for file modes
    'DOT',
)

# Regular expression rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_DOT = r'\.'
t_ASSIGN = r'='

# Ignore whitespace and tabs
t_ignore = ' \t'

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Keywords
reserved = {
    'open': 'OPEN',
    'read': 'READ',
    'write': 'WRITE',
    'close': 'CLOSE',
}

# Mode specifications
modes = {
    '"r"': 'MODE',
    '"w"': 'MODE',
    '"a"': 'MODE',
    '"rb"': 'MODE',
    '"wb"': 'MODE',
    '"ab"': 'MODE',
    '"r+"': 'MODE',
    '"w+"': 'MODE',
    '"a+"': 'MODE',
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    if t.value in modes:
        t.type = 'MODE'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build lexer
lexer = lex.lex()

# Parsing rules
def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                 | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : file_operation'''
    p[0] = p[1]

def p_file_operation(p):
    '''file_operation : open_operation
                     | read_operation
                     | write_operation
                     | close_operation'''
    p[0] = p[1]

def p_open_operation(p):
    '''open_operation : IDENTIFIER ASSIGN OPEN LPAREN STRING RPAREN
                     | IDENTIFIER ASSIGN OPEN LPAREN STRING COMMA MODE RPAREN'''
    if len(p) == 7:
        p[0] = {
            'type': 'open',
            'variable': p[1],
            'filename': p[5],
            'mode': '"r"'  # default mode
        }
    else:
        p[0] = {
            'type': 'open',
            'variable': p[1],
            'filename': p[5],
            'mode': p[7]
        }

def p_read_operation(p):
    '''read_operation : IDENTIFIER DOT READ LPAREN RPAREN
                     | IDENTIFIER DOT READ LPAREN NUMBER RPAREN'''
    if len(p) == 6:
        p[0] = {
            'type': 'read',
            'file': p[1],
            'size': -1  # Read all
        }
    else:
        p[0] = {
            'type': 'read',
            'file': p[1],
            'size': p[5]
        }

def p_write_operation(p):
    '''write_operation : IDENTIFIER DOT WRITE LPAREN STRING RPAREN
                      | IDENTIFIER DOT WRITE LPAREN IDENTIFIER RPAREN'''
    p[0] = {
        'type': 'write',
        'file': p[1],
        'data': p[5]
    }

def p_close_operation(p):
    '''close_operation : IDENTIFIER DOT CLOSE LPAREN RPAREN'''
    p[0] = {
        'type': 'close',
        'file': p[1]
    }

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lexer.lineno}")
    else:
        print("Syntax error at EOF")

# Build parser
parser = yacc.yacc()

def validate_file_operation(code):
    """Validate file operation syntax and return AST if valid"""
    try:
        ast = parser.parse(code)
        return True, ast
    except Exception as e:
        return False, str(e)

def main():
    print("File Operations Syntax Validator")
    print("Example operations:")
    print("- f = open(\"file.txt\", \"r\")")
    print("- f = open(\"file.txt\")")
    print("- f.read()")
    print("- f.read(100)")
    print("- f.write(\"Hello\")")
    print("- f.close()")
    
    while True:
        try:
            print("\nOptions:")
            print("1. Validate file operation")
            print("2. Exit")
            choice = input("Enter choice (1-2): ")
            
            if choice == '1':
                code = input('Enter file operation: ')
                if not code:
                    continue
                
                is_valid, result = validate_file_operation(code)
                if is_valid:
                    print("Valid file operation!")
                    print("AST:", result)
                else:
                    print("Invalid file operation!")
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

if __name__ == '__main__':
    main()