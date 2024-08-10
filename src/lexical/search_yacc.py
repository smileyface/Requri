import logging

import ply.yacc as yacc
from src.lexical.search_lex import tokens
import src.lexical.search_operations as search_operations


# Define grammar rules
def p_expression(p):
    '''
    expression : tag_list
               | tag_list APPEND tag_list
               | tag_list APPEND title_list
               | title_list
               | title_list APPEND title_list
               | title_list APPEND tag_list
               | ALL

    '''
    if len(p) == 2:
        logging.info(f"Parsing expression:{p[1]}")
        if p[1] == "all":
            p[0] = search_operations.get_all()
        else:
            p[0] = p[1]
    elif len(p) == 4:
        if p[2] == "+":
            p[0] = list(set(p[1] + p[3]))




def p_title_list(p):
    '''title_list : TITLE ARG_VALUE
                  | title_list TITLE ARG_VALUE
                  | TITLE EMPTY_ARG
                  | title_list TITLE EMPTY_ARG
    '''

    if p.slice[1].type == "TITLE":
        if p[2] == "[]":
            pass
        else:
            p[0] = search_operations.get_titles(p[2])
    elif p.slice[1].type == "title_list":
        current_list = []
        if p[3] == "[]":
            pass
        else:
            current_list = p.slice[1].value + search_operations.get_titles(p[3])
        p[0] = list(set(current_list))
    logging.info(f"Parsing title_list: {p[2]} found {len(p[0])} objects with that title")


def p_tag_list(p):
    '''
    tag_list : TAG ARG_VALUE
             | tag_list TAG ARG_VALUE
             | TAG EMPTY_ARG
             | tag_list TAG EMPTY_ARG
    '''
    if p.slice[1].type == "TAG":
        if p[2] == "[]":
            p[0] = search_operations.get_tagged()
        else:
            p[0] = search_operations.get_tags(p[2])
    elif p.slice[1].type == "tag_list":
        current_list = []
        if p[3] == "[]":
            current_list = p.slice[1].value + search_operations.get_tagged()
        else:
            current_list = p.slice[1].value + search_operations.get_tags(p[3])
        p[0] = list(set(current_list))
    logging.info(f"Parsing tag_list: {p[2]} found {len(p[0])} objects with that tag")


def p_error(p):
    raise SyntaxError(f"Syntax error at: {p}")


# Build the parser
parser = yacc.yacc(debug=True)
