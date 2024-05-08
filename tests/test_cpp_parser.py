import unittest
import os

from parsers.code.source_cpp import cpp_parser
from structures import project
from tests.harness import Requiri_Harness


class TestHarness(Requiri_Harness):
    def setUp(self):
        super.setUp()
        self.parser = cpp_parser()  # Directory to save the test files

    def tearDown(self):
        # Clean up test files after each test
        test_directory = "test_files"
        for file_name in os.listdir(test_directory):
            file_path = os.path.join(test_directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(test_directory)

    def test_scan_cpp_files(self):
        # Directory to scan for .cpp and .h files
        directory = "test_files"

        # Test the scan_cpp_files method
        self.parser.scan_cpp_files(directory)
        self.assertGreater(len(self.parser.cpp_files), 0)

    def test_find_functions(self):
        # Directory to scan for .cpp and .h files
        directory = "test_files"

        # Get a list of .cpp and .h files in the directory
        self.parser.scan_cpp_files(directory)

        # Test the find_functions method for each file
        for file_path in self.parser.cpp_files:
            self.parser.parse(file_path)
            self.assertGreater(len(self.parser.functions), 0)

        for x in self.parser.functions:
            x = x.signature
            if x not in list_of_function_signatures:
                self.fail(f"Unknown function found {x}")
            list_of_function_signatures.remove(x)
        self.assertEqual(len(list_of_function_signatures), 0,
                         f"Functions not discovered {', '.join(list_of_function_signatures)}")

    def test_find_callers_of_function(self):
        # Directory to scan for .cpp and .h files
        directory = "test_files"

        # Get a list of .cpp and .h files in the directory
        self.parser.scan_cpp_files(directory)

        # Test the find_functions method for each file
        for file_path in self.parser.cpp_files:
            self.parser.parse(file_path)
            self.assertGreater(len(self.parser.functions), 0)

        function_calls = self.parser.function_calls

        self.assertTrue(len(function_calls) > 0)  # Assert that at least 1 call was found.
