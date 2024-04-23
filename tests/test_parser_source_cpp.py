import os
import unittest

from parsers.source_cpp import cpp_parser, generate_code_list
from structures import project
from structures.code import code_list


class Testcpp_parser(unittest.TestCase):

    def generate_test_cpp_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write("#include <iostream>\n\n")
            file.write("void global_function() {\n")
            file.write("\tstd::cout << \"This is a global function.\" << std::endl;\n")
            file.write("}\n\n")
            file.write("class MyClass {\n")
            file.write("public:\n")
            file.write("\tvoid member_function1() {\n")
            file.write("\t\tstd::cout << \"This is member function 1.\" << std::endl;\n")
            file.write("\t}\n\n")
            file.write("\tvoid member_function2() const {\n")
            file.write("\t\tstd::cout << \"This is member function 2.\" << std::endl;\n")
            file.write("\t}\n\n")
            file.write("};\n\n")

        # Directory to save the test files
        test_directory = "test_files"

        # Create the test directory if it doesn't exist
        if not os.path.exists(test_directory):
            os.makedirs(test_directory)

        # Generate test files
        for i in range(3):
            file_name = f"test_file_{i}.cpp"
            file_path = os.path.join(test_directory, file_name)
            self.generate_test_cpp_file(file_path)
            print(f"Generated test file: {file_path}")

    def test_find_functions(self):
        parser = cpp_parser()
        # Directory to scan for .cpp and .h files
        project.set_code_location("C:\\Users\\kason\\source\\repos\\ContraControl\\dev")

        # Get a list of .cpp and .h files in the directory
        cpp_files = parser.cpp_files

        functions = []
        # Test the find_functions method for each file
        for file_path in cpp_files:
            functions.extend(parser.find_functions(file_path))

        self.assertTrue(len(functions) > 0)  # Assert that at least one function was found

        self.functions = functions

    def test_scan_cpp_files(self):
        # Create an instance of cpp_parser
        parser = cpp_parser()

        # Directory to scan for .cpp and .h files
        project.set_code_location("C:\\Users\\kason\\source\\repos\\ContraControl\\dev")

        # Test the scan_cpp_files method
        cpp_files = parser.cpp_files
        self.assertTrue(len(cpp_files) > 0)  # Assert that at least one file was found

    def test_find_callers_of_function(self):

        project.set_code_location("C:\\Users\\kason\\source\\repos\\ContraControl\\dev")

        def print_results(current, final):
            print(f"{current}/{final} files scanned")
        generate_code_list(print_results)

        called = []
        for x in list(code_list.values()):
            called.extend(x.call_list)


        self.assertTrue(len(called) > 0)  # Assert that at least 1 call was found.

    def test_get_functions_from_source(self):

        project.set_code_location("C:\\Users\\kason\\source\\repos\\ContraControl\\dev")

        def print_results(current, final):
            print(f"{current}/{final} files scanned")
        generate_code_list(print_results)

# Run the tests
if __name__ == '__main__':
    unittest.main()
