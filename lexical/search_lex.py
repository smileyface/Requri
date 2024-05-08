import ply.lex as lex

# Define tokens
tokens = (
    'TAG',
    'TITLE',
    'ARG_VALUE',
    'EMPTY_ARG',
    'APPEND'
)

# Define regex for tokens
t_TAG = r'tag'
t_TITLE = r'title'
t_APPEND = r'\+'
t_EMPTY_ARG = r'\[\]'

# Define a rule for ARG_VALUE to strip the brackets
def t_ARG_VALUE(t):
    r'\[(\w+\s?)+\]'
    t.value = t.value[1:-1]  # Strip the brackets
    return t

# Define error handling
def t_error(t):
    t.lexer.skip(1)


# Define ignored characters
t_ignore = ' \t\n'

# Build the lexer
lexer = lex.lex()
