import ply.yacc as yacc
from lexical.search_lex import tokens
import lexical.search_operations as search_operations

# Define grammar rules
def p_expression(p):
    '''
    expression : tag_list TITLE ARG_VALUE
               | tag_list
               | TITLE ARG_VALUE
               | TITLE
               | tag_list APPEND tag_list
               | tag_list APPEND TITLE
    '''
    print("Parsing expression:", p[1])
    p[0] = p[1]



def p_tag_list(p):
    '''
    tag_list : TAG ARG_VALUE
             | tag_list TAG ARG_VALUE
    '''
    p[0] = search_operations.get_tags(p[2])
    print(f"Parsing tag_list: {p[2]} found {len(p[0])} objects with that tag")

def p_error(p):
    print("Syntax error at:", p)

# Build the parser
parser = yacc.yacc()