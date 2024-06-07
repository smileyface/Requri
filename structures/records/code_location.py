import os

class Code_Location:
    DEFINITION = 0
    DECLARATION = 1

    def __init__(self, location_type: int, file: str, begin: int, end: int) -> None:
        """
        Initializes an instance of the Code_Location class.

        Args:
            type (int): An integer representing the type of code location.
            file (str): A string representing the file name or path.
            begin (int): The starting line number.
            end (int): The ending line number.
        """

        self.type = location_type
        self.file = os.path.abspath(file)
        if location_type not in [Code_Location.DEFINITION, Code_Location.DECLARATION]:
            raise ValueError("Invalid type parameter")
        if begin < 0 or end < 0 or begin > end:
            raise ValueError("Invalid begin or end values")
        self.begin = begin
        self.end = end