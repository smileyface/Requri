import os
import clang.cindex

from structures import project
from structures.code import Code, code_list, append, signature_to_id_map

# Set the library path for clang
clang.cindex.Config.set_library_path("C:\\Program Files\\LLVM\\bin")

def generate_code_list(callback):
    parser = cpp_parser()
    functions = parser.get_functions_from_source(project.get_code_location(), callback)
    for x in functions:
        append(x)
    print(f"{len(code_list)} functions found.")
    for y in parser.cpp_files:
        print(f"Searching in {y}")
        calls = parser.find_function_calls(y)
        for z in calls.keys():
            print(f"\tCall to {z} found")
            code_list[signature_to_id_map[z]].call_list.extend(calls[z])



class cpp_parser:
    def __init__(self):
        self._cpp_files = []

    @property
    def cpp_files(self):
        if self._cpp_files == []:
            self.scan_cpp_files(project.get_code_location())
        return self._cpp_files

    def find_functions(self, file_path):
        # Initialize Clang index
        index = clang.cindex.Index.create()

        # Parse the file
        translation_unit = index.parse(file_path)

        # Helper function to extract functions from the translation unit's cursor
        def extract_functions(cursor, class_names=None):
            if class_names is None:
                class_names = []
            functions = []
            for child in cursor.get_children():
                spelling = None
                if child.location.file and child.location.file.name == file_path:
                    if child.kind == clang.cindex.CursorKind.FUNCTION_DECL:
                        # Extract function name
                        function_name = child.spelling
                        # Extract function arguments
                        arguments = [arg.type.spelling for arg in child.get_arguments()]
                        # Append function signature to functions list
                        functions.append(Code(file_path, "global", child.semantic_parent.spelling, function_name,
                                              arguments, child.extent.start.line, child.extent.end.line))
                    elif child.kind == clang.cindex.CursorKind.CXX_METHOD:
                        # Extract method name
                        method_name = child.spelling
                        # Extract class name
                        class_name = child.semantic_parent.spelling
                        # Extract method arguments' types
                        arguments = [arg.type.spelling for arg in child.get_arguments()]
                        # Append method signature to functions list
                        access_level = "public"
                        if child.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
                            access_level = "protected"
                        elif child.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
                            access_level = "private"
                        functions.append(Code(file_path, access_level, class_name, method_name, arguments,
                                              child.extent.start.line, child.extent.end.line))
                    functions.extend(extract_functions(child, class_names))

            return functions

        # Extract functions from the translation unit's cursor
        functions = extract_functions(translation_unit.cursor)

        return functions

    def find_function_calls(self, file_path):
        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_path)
        calls = dict()

        def traverse(cursor, parent_cursor=None):
            if cursor.location.file and project.get_code_location() in cursor.location.file.name:
                if cursor.kind == clang.cindex.CursorKind.CALL_EXPR:
                    called_function = cursor.referenced
                    if called_function:
                        for target_func in list(code_list.values()):
                            if (called_function.spelling == target_func.name and
                                    called_function.semantic_parent.spelling == target_func.class_name):
                                parent_function = find_parent_function(cursor)
                                if parent_function:
                                    if target_func.signature in calls.keys():
                                        # Extract function signature and append to calls
                                        calls[target_func.signature].append(parent_function.signature)
                                    else:
                                        calls[target_func.signature] = [parent_function.signature]
            for child in cursor.get_children():
                try:
                    traverse(child, cursor)
                except ValueError as e:
                    continue

        def find_parent_function(cursor):
            for x in code_list.keys():
                if (os.path.normpath(code_list[x].location) == cursor.location.file.name and
                        (code_list[x].func_begin < cursor.location.line < code_list[x].func_end)):
                    return code_list[x]
            return None

        def get_function_signature(cursor):
            # Extract function signature from the cursor
            function_name = cursor.spelling
            result_type = cursor.result_type.spelling
            parameters = [param.type.spelling for param in cursor.get_children() if
                          param.kind == clang.cindex.CursorKind.PARM_DECL]
            signature = f"{result_type} {function_name}({', '.join(parameters)})"
            return signature

        traverse(translation_unit.cursor)
        return calls

    def scan_cpp_files(self, directory):
        self._cpp_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".cpp") or file.endswith(".h"):
                    self._cpp_files.append(os.path.join(root, file))

    def get_functions_from_source(self, directory, callback):
        # Get a list of .cpp and .h files in the directory
        functions = []
        for x in range(len(self.cpp_files)):
            functions.extend(self.find_functions(self.cpp_files[x]))
            callback(x, len(self.cpp_files))
        return functions

    def get_callers_of_function(self, directory):
        cpp_files = self.scan_cpp_files(directory)
        callers = []
        for file_path in cpp_files:
            print(f"Scanning: {file_path}")
            calls = self.find_function_calls(file_path)
            if calls:
                callers.extend(calls)
        return callers
