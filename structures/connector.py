from structures.code import Code


def connect(connect1, connect2):
    connect2.connect(type(connect1).__name__, connect1)
    connect1.connect(type(connect2).__name__, connect2)
