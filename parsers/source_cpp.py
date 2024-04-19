import os
import clang.cindex


class cpp_parser:
    def __init__(self):
        # Set the library path for clang
        clang.cindex.Config.set_library_path("C:\\Program Files\\LLVM\\bin")

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
                        if file_path not in child.semantic_parent.spelling:
                            spelling = f"{child.semantic_parent.spelling}::{child.spelling}"
                        else:
                            spelling = child.spelling
                    elif child.kind == clang.cindex.CursorKind.CXX_METHOD:
                        if file_path not in child.semantic_parent.spelling:
                            spelling = f"{child.semantic_parent.spelling}::{child.spelling}"
                        else:
                            spelling = child.spelling
                        if child.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
                            spelling = f"protected::" + spelling
                        elif child.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
                            spelling = f"private::" + spelling
                    if spelling:
                        functions.append((child.location.file.name, spelling))
                    functions.extend(extract_functions(child, class_names))

            return functions

        # Extract functions from the translation unit's cursor
        functions = extract_functions(translation_unit.cursor)

        return functions

    def scan_cpp_files(self, directory):
        cpp_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".cpp") or file.endswith(".h"):
                    cpp_files.append(os.path.join(root, file))
        return cpp_files

    def get_functions_from_source(self, directory, callback):
        # Get a list of .cpp and .h files in the directory
        cpp_files = self.scan_cpp_files(directory)
        functions = []
        for x in range(len(cpp_files)):
            functions = self.find_functions(cpp_files[x])
            callback(x, len(cpp_files))
        return functions
