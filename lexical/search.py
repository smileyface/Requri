from lexical.search_lex import lexer
from lexical.search_yacc import parser


# Define a function to interpret the input string
def interpret(input_string):
    # Tokenize input string
    lexer.input(input_string)

    # Parse tokens
    for token in lexer:
        print(token)

    # Parse input string
    result = parser.parse(input_string)
    print(result)
    return result



