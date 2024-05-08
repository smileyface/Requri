_code_list = dict()
signature_to_id_map = dict()


def append(code):
    global _code_list
    _code_list[code.unique_id] = code
    signature_to_id_map[code.signature] = code.unique_id


def get_files(parser):
    list_of_files = set()
    for x in parser.functions:
        list_of_files.add()


def get_code_list():
    return _code_list


def add_code_to_list(functions):
    for x in functions:
        append(x)


def add_code_to_source(cpp_files, functions):
    for x in cpp_files:
        for function in functions:
            if function.definition == x or function.declaration == x:
                x.functions.append(function)


def add_calls_to_source(cpp_files, function_calls):
    def get_parent(function_call):
        for file in cpp_files:
            if file.full_path == function_call[0]:
                for function in file.functions:
                    if function.func_begin < function_call[1] < function.func_end:
                        return function

    for x in function_calls:
        called_function_signature = f"{x[2]}::{x[3]}({', '.join(x[4])})"
        if called_function_signature in signature_to_id_map.keys():
            parent = get_parent(x)
            if parent:
                _code_list[signature_to_id_map[called_function_signature]].call_list.append(parent)


def generate_code_list(parser):
    cpp_files, functions, function_calls = parser
    add_code_to_list(functions)
    add_code_to_source(cpp_files, functions)
    add_calls_to_source(cpp_files, function_calls)
