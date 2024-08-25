# code_list.py

# Module-level variables to store the code list and the signature-to-ID map
_code_list = {}
_signature_to_id_map = {}

def append(code):
    """
    Appends a code object to the code list and updates the signature-to-ID map.

    Parameters:
    code (object): The code object to append.
    """
    _code_list[code.unique_id] = code
    _signature_to_id_map[code.signature] = code.unique_id

def get_files(parser):
    """
    Extracts and returns a set of files from the parser's functions.

    Parameters:
    parser (object): The parser object containing functions.

    Returns:
    set: A set of files extracted from the parser's functions.
    """
    list_of_files = set()
    for x in parser.functions:
        list_of_files.add(x)  # Assuming you want to add x to the set
    return list_of_files

def get_code_list():
    """
    Returns the list of all code objects.

    Returns:
    list: The list of code objects.
    """
    return list(_code_list.values())

def add_code_to_list(functions):
    """
    Adds multiple code objects to the code list.

    Parameters:
    functions (iterable): An iterable of code objects to append.
    """
    for x in functions:
        append(x)

def add_code_to_source(cpp_files, functions):
    """
    Associates code objects with their corresponding source files.

    Parameters:
    cpp_files (iterable): An iterable of source files.
    functions (iterable): An iterable of functions to associate with source files.
    """
    for x in cpp_files:
        for function in functions:
            if function.definition == x or function.declaration == x:
                x.functions.append(function)

def add_calls_to_source(cpp_files, function_calls):
    """
    Associates function calls with their parent functions in the source files.

    Parameters:
    cpp_files (iterable): An iterable of source files.
    function_calls (iterable): An iterable of function call details.
    """
    def get_parent(function_call):
        for file in cpp_files:
            if file.full_path == function_call[0]:
                for function in file.functions:
                    if function.func_begin < function_call[1] < function.func_end:
                        return function

    for x in function_calls:
        called_function_signature = f"{x[2]}::{x[3]}({', '.join(x[4])})"
        if called_function_signature in _signature_to_id_map.keys():
            parent = get_parent(x)
            if parent:
                _code_list[_signature_to_id_map[called_function_signature]].call_list.append(parent)

def generate_code_list(parser):
    """
    Generates a code list based on the parser output.

    Parameters:
    parser (tuple): A tuple containing cpp_files, functions, and function_calls.
    """
    cpp_files, functions, function_calls = parser
    add_code_to_list(functions)
    add_code_to_source(cpp_files, functions)
    add_calls_to_source(cpp_files, function_calls)
