import os
import re
import tokenize


def list_test_methods(directory_path):
    test_methods = []
    test_method_pattern = re.compile(r"^\s*def (test_\w+)\(")
    class_pattern = re.compile(r"^\s*class (\w+)\(*\w*\)*:")


    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    tokens = tokenize.tokenize(f.readline)
                    class_name = None
                    method_name = None

                    for token in tokens:
                        if token.type == tokenize.NAME and token.string == 'class':
                            # Get the class name
                            token = next(tokens)
                            if token.type == tokenize.NAME:
                                class_name = token.string

                        if token.type == tokenize.NAME and token.string == 'def':
                            # Get the function name
                            token = next(tokens)
                            if token.type == tokenize.NAME:
                                method_name = token.string
                                if method_name.startswith('test_'):
                                    test_methods.append((file, class_name, method_name))


    return test_methods


def remove_test_class(test_methods, test_class):
    stripped_methods = []
    for method in test_methods:
        add = True
        for x in test_class:
            if method[1] == x:
                add = False
        if add:
            stripped_methods.append(method)
    return stripped_methods


if __name__ == "__main__":
    test_methods = remove_test_class(list_test_methods("../tests/tests"), ["MockEvent", "FaultyCode"])

    # Print the test methods for verification
    for file, class_name, method_name in test_methods:
        print(f"File: {file}, Class: {class_name}, Method: {method_name}")