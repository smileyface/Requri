class CodeManager:
    def __init__(self):
        self._code_list = {}
        self.signature_to_id_map = {}

    def append(self, code):
        self._code_list[code.unique_id] = code
        self.signature_to_id_map[code.signature] = code.unique_id

    def get_files(self, parser):
        list_of_files = set()
        for x in parser.functions:
            list_of_files.add(x)  # Assuming you want to add x to the set

    def get_code_list(self):
        return list(self._code_list.values())

    def add_code_to_list(self, functions):
        for x in functions:
            self.append(x)

    def add_code_to_source(self, cpp_files, functions):
        for x in cpp_files:
            for function in functions:
                if function.definition == x or function.declaration == x:
                    x.functions.append(function)

    def add_calls_to_source(self, cpp_files, function_calls):
        def get_parent(function_call):
            for file in cpp_files:
                if file.full_path == function_call[0]:
                    for function in file.functions:
                        if function.func_begin < function_call[1] < function.func_end:
                            return function

        for x in function_calls:
            called_function_signature = f"{x[2]}::{x[3]}({', '.join(x[4])})"
            if called_function_signature in self.signature_to_id_map.keys():
                parent = get_parent(x)
                if parent:
                    self._code_list[self.signature_to_id_map[called_function_signature]].call_list.append(parent)

    def generate_code_list(self, parser):
        cpp_files, functions, function_calls = parser
        self.add_code_to_list(functions)
        self.add_code_to_source(cpp_files, functions)
        self.add_calls_to_source(cpp_files, function_calls)