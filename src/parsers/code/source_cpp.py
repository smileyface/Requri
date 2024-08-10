import concurrent
import os
import threading

import clang.cindex

from src.structures import project
from src.structures.lists import file_list
from src.structures.records.code import Code
from src.structures.source_file import File

# Set the library path for clang
clang.cindex.Config.set_library_path("C:\\Program Files\\LLVM\\bin")

mutex = threading.Lock()


def parse():
    parser = cpp_parser()
    parser.parse_code_base()
    return (parser.cpp_files, parser.functions, parser.function_calls)

class cpp_parser:
    _function_calls = []
    _file_function_map = dict()
    _functions = []

    def __init__(self):
        pass

    @property
    def cpp_files(self):
        if not self._cpp_files:
            self.scan_cpp_files(project.get_code_location())
        return self._cpp_files

    @property
    def functions(self):
        if not self._functions:
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

    def map_functions_to_files(self):
        if self._file_function_map == {}:
            for x in self._functions:
                if x.location in self._file_function_map:
                    self._file_function_map[x.location] = [x.unique_id]
                else:
                    self._file_function_map[x.location].append(x.unique_id)

    # Helper function to extract functions from the translation unit's cursor
    def extract_functions(self, cursor, file_path, class_names=None):
        if class_names is None:
            class_names = []
        functions = []
        calls = []
        for child in cursor.get_children():
            if child.location.file and child.location.file.name == file_path.full_path:
                if child.kind == clang.cindex.CursorKind.FUNCTION_DECL:
                    # Extract function name
                    function_name = child.spelling
                    # Extract function arguments
                    arguments = [arg.type.spelling for arg in child.get_arguments()]
                    signature = f"{child.semantic_parent.spelling}::{function_name}({', '.join(arguments)})"
                    # Append function signature to functions list
                    existing_function = next((func for func in self._functions if func.signature == signature), None)
                    if existing_function:
                        if child.is_definition():
                            # Update the existing function with the definition status
                            existing_function.definition = file_path
                        else:
                            existing_function.declaration = file_path
                    else:
                        functions.append(Code(file_path, "global", child.semantic_parent.spelling, function_name,
                                              arguments, child.extent.start.line, child.extent.end.line,
                                              child.is_definition()))
                        print(f"{functions[-1].signature} found")
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
                    signature = f"{class_name}::{method_name}({', '.join(arguments)})"
                    existing_function = next((func for func in self._functions if func.signature == signature), None)
                    if existing_function:
                        if child.is_definition():
                            # Update the existing function with the definition status
                            existing_function.definition = file_path
                            print(f"{existing_function.signature} definition found")
                        else:
                            existing_function.declaration = file_path
                            print(f"{existing_function.signature} declaration found")
                    else:
                        functions.append((Code(file_path, access_level, class_name, method_name, arguments,
                                                child.extent.start.line, child.extent.end.line, child.is_definition())))
                        print(f"{functions[-1].signature} found")
                elif child.kind == clang.cindex.CursorKind.CONSTRUCTOR:
                    # Extract class name
                    class_name = child.semantic_parent.spelling
                    # Extract method arguments' types
                    arguments = [arg.type.spelling for arg in child.get_arguments()]
                    # Append constructor signature to functions list
                    signature = f"{class_name}::{class_name}({', '.join(arguments)})"
                    existing_function = next((func for func in self._functions if func.signature == signature),
                                             None)
                    if existing_function:
                        if child.is_definition():
                            # Update the existing function with the definition status
                            existing_function.definition = file_path
                            print(f"{existing_function.signature} definition found")
                        else:
                            existing_function.declaration = file_path
                            print(f"{existing_function.signature} declaration found")
                    else:
                        functions.append((Code(file_path, "public", class_name, class_name, arguments,
                                               child.extent.start.line, child.extent.end.line,
                                               child.is_definition())))
                        print(f"{functions[-1].signature} found")
                elif cursor.kind == clang.cindex.CursorKind.CALL_EXPR:
                    called_function = cursor.referenced
                    if called_function:
                        calls.append(
                            (cursor.location.file.name, cursor.location.line, called_function.semantic_parent.spelling,
                             called_function.spelling, [arg.type.spelling for arg in called_function.get_arguments()]))
                        print(
                            f"\tCall to {called_function.semantic_parent.spelling}::{called_function.spelling}({', '.join(calls[-1][4])})")
                elif cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
                    # Check if the cursor's children include the member access operator (->)
                    pointed_to_function = cursor.referenced
                    if pointed_to_function and pointed_to_function.kind in [clang.cindex.CursorKind.FUNCTION_DECL,
                                                                            clang.cindex.CursorKind.CXX_METHOD]:
                        calls.append(
                            (cursor.location.file.name, cursor.location.line,
                             pointed_to_function.semantic_parent.spelling,
                             pointed_to_function.spelling,
                             [arg.type.spelling for arg in pointed_to_function.get_arguments()]))
                _calls, _functions = self.extract_functions(child, file_path, class_names)
                calls.extend(_calls)
                functions.extend(_functions)

        # Convert each element of the calls list to a tuple before adding to the set
        # Convert each element of the calls list to a tuple before adding to the set
        unique_calls = set()
        for call in calls:
            try:
                # Convert the list of arguments to a tuple
                arguments_tuple = tuple(call[4])
                # Create a new tuple for the call with the arguments tuple included
                call_tuple = tuple(call[:4]) + (arguments_tuple,)
                # Add the call tuple to the set
                unique_calls.add(call_tuple)
            except TypeError:
                # If conversion to tuple fails, handle the unhashable type differently
                print(f"Ignoring unhashable call: {call}")

        # Convert set back to list if necessary
        calls = list(unique_calls)
        return calls, functions

    def extract_function_calls(self, cursor, file_name):
        calls = []
        if cursor.location.file and cursor.location.file.name == file_name.full_path:
            line_number = ""
            if cursor.extent.start.line == cursor.extent.end.line:
                line_number = f"{cursor.extent.start.line}"
            else:
                line_number = f"{cursor.extent.start.line}-{cursor.extent.end.line}"

        for child in cursor.get_children():
            try:
                if child.location.file and child.location.file.name == file_name.full_path:
                    calls.extend(self.extract_function_calls(child, file_name))
            except ValueError as e:
                continue
        return calls

    def find_functions(self, file_path):
        print(f"Searching for functions in: {file_path.full_path}")
        # Initialize Clang index
        index = clang.cindex.Index.create()

        # Parse the file
        translation_unit = index.parse(file_path)

        # Extract functions from the translation unit's cursor
        functions = self.extract_functions(translation_unit.cursor, file_path)
        mutex.acquire()
        self._functions.extend(functions)
        mutex.release()

    def find_function_calls(self, file_path):
        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_path)
        calls = dict()
        print(f"Finding calls in {file_path}")

        self.extract_function_calls(translation_unit.cursor)

    def scan_cpp_files(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".cpp") or file.endswith(".h"):
                    file_list.add_file(File(os.path.join(root, file)))

    def get_functions_from_source(self, callback):
        # Get a list of .cpp and .h files in the directory
        functions = []
        for x in range(len(self.cpp_files)):
            functions.extend(self.find_functions(self.cpp_files[x]))
            print(f"{x}/{len(self.cpp_files)} files scanned")
        return functions

    def parse(self, file):
        print(f"Searching for functions in: {file.path}")
        # Initialize Clang index
        index = clang.cindex.Index.create()
        translation_unit = None
        if (file.full_path[-2:] == ".h"):
            translation_unit = index.parse(file.full_path, ['-x', 'c++-header'])
        else:
            translation_unit = index.parse(file.full_path)

        # Extract functions from the translation unit's cursor
        function_calls, functions = self.extract_functions(translation_unit.cursor, file)
        mutex.acquire()
        self._functions.extend(functions)
        self._function_calls.extend(function_calls)
        mutex.release()

    def parse_code_base(self):
        for x in self.cpp_files:
            self.parse(x)
