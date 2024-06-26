from lexical.search_lex import lexer
from lexical.search_yacc import parser


# Define a function to interpret the input string
def interpret(input_string):
    # Tokenize input string
    lexer.input(input_string)

    # Parse input string
    result = parser.parse(input_string)
    print(f"Found {len(result)} records")
    return result



