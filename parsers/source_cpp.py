import concurrent
import os
import threading

import clang.cindex

from structures import project
from structures.code import Code, code_list, append, signature_to_id_map

# Set the library path for clang
clang.cindex.Config.set_library_path("C:\\Program Files\\LLVM\\bin")

mutex = threading.Lock()

def generate_code_list():
    parser = cpp_parser()
    for x in parser.functions:
        append(x)
    calls = parser.function_calls
    for z in calls.keys():
        print(f"\tCall to {z} found")
        code_list[signature_to_id_map[z]].call_list.extend(calls[z])


class cpp_parser:
    _function_calls = dict()
    _cpp_files = []
    _functions = []

    def __init__(self):
        pass

    @property
    def cpp_files(self):
        if self._cpp_files == []:
            self.scan_cpp_files(project.get_code_location())
        return self._cpp_files

    @property
    def functions(self):
        if self._functions == []:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.find_functions, file_path) for file_path in self.cpp_files]
                concurrent.futures.wait(futures)
            print(f"{len(self._functions)} functions found")
        return self._functions

    @property
    def function_calls(self):
        self.functions
        if self._function_calls == {}:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.find_function_calls, file_path) for file_path in self.cpp_files]
                concurrent.futures.wait(futures)
        return self._function_calls

    def find_functions(self, file_path):
        print(f"Searching for functions in: {file_path}")
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
        mutex.acquire()
        self._functions.extend(functions)
        mutex.release()

    def find_function_calls(self, file_path):
        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_path)
        calls = dict()
        print(f"Finding calls in {file_path}")

        def traverse(cursor, parent_cursor=None):
            if cursor.location.file and project.get_code_location() in cursor.location.file.name:
                if cursor.kind == clang.cindex.CursorKind.CALL_EXPR:
                    called_function = cursor.referenced
                    if called_function:
                        functions = self.functions
                        for target_func in functions:
                            if (called_function.spelling == target_func.name and
                                    called_function.semantic_parent.spelling == target_func.class_name):
                                parent_function = find_parent_function(cursor)
                                if parent_function:
                                    print(f"Call to {target_func.signature} found")
                                    mutex.acquire()
                                    if target_func.signature in calls.keys():
                                        # Extract function signature and append to calls
                                        self._function_calls[target_func.signature].append(parent_function.signature)
                                    else:
                                        self._function_calls[target_func.signature] = [parent_function.signature]
                                    mutex.release()
            for child in cursor.get_children():
                try:
                    traverse(child, cursor)
                except ValueError as e:
                    continue

        def find_parent_function(cursor):
            for x in self.functions:
                if (os.path.normpath(x.location) == cursor.location.file.name and
                        (x.func_begin < cursor.location.line < x.func_end)):
                    return x
            return None

        traverse(translation_unit.cursor)

    def scan_cpp_files(self, directory):
        self._cpp_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".cpp") or file.endswith(".h"):
                    self._cpp_files.append(os.path.join(root, file))

    def get_functions_from_source(self, callback):
        # Get a list of .cpp and .h files in the directory
        functions = []
        for x in range(len(self.cpp_files)):
            functions.extend(self.find_functions(self.cpp_files[x]))
            print(f"{x}/{len(self.cpp_files)} files scanned")
        return functions

    def get_callers_of_function(self, directory):
        cpp_files = self.scan_cpp_files(directory)
        callers = []
        for file_path in cpp_files:
            calls = self.find_function_calls(file_path)
            if calls:
                callers.extend(calls)
        return callers
