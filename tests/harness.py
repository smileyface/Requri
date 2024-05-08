import os
import unittest

from structures import project

def generate_test_cpp_file(directory):
    # Create the test directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # File 1: basic.cpp
    basic_content = """
    #include <iostream>

    // Global function
    void global_function() {
        std::cout << "This is a global function." << std::endl;
    }

    // Class definition
    class MyClass {
    public:
        // Member function without arguments
        void member_function1() {
            global_function()
            std::cout << "This is member function 1." << std::endl;
        }

        // Member function with constant qualifier
        void member_function2() const {
            std::cout << "This is member function 2." << std::endl;
        }
    };
    """
    with open(os.path.join(directory, "basic.cpp"), "w") as file:
        file.write(basic_content)

    # File 2: math.cpp
    math_content = """
    #include <iostream>

    namespace Math {
        // Function to add two numbers
        int add(int a, int b) {
            return a + b;
        }

        // Function to subtract two numbers
        int subtract(int a, int b) {
            return a - b;
        }
    }
    """
    with open(os.path.join(directory, "math.cpp"), "w") as file:
        file.write(math_content)

    # File 3: shapes.cpp
    shapes_content = """
    #include <iostream>

    // Base class for shapes
    class Shape {
    public:
        // Virtual function to calculate area
        virtual double area() const = 0;

        // Function to display shape information
        virtual void display_info() const {
            std::cout << "This is a shape." << std::endl;
        }
    };

    // Derived class: Rectangle
    class Rectangle : public Shape {
    private:
        double width;
        double height;

    public:
        Rectangle(double w, double h) : width(w), height(h) {}

        // Implementation of area function for rectangle
        double area() const override {
            return width * height;
        }

        // Overridden display_info function for rectangle
        void display_info() const override {
            std::cout << "Rectangle: width = " << width << ", height = " << height << std::endl;
        }
    };

    // Derived class: Circle
    class Circle : public Shape {
    private:
        double radius;

    public:
        Circle(double r) : radius(r) {}

        // Implementation of area function for circle
        double area() const override {
            return 3.14159 * radius * radius;
        }

        // Overridden display_info function for circle
        void display_info() const override {
            std::cout << "Circle: radius = " << radius << std::endl;
        }
    };
    """
    with open(os.path.join(directory, "shapes.cpp"), "w") as file:
        file.write(shapes_content)


list_of_function_signatures = ["test_files\\basic.cpp::global_function()",
                               "MyClass::member_function1()",
                               "MyClass::member_function2()",
                               "Math::add(int, int)",
                               "Math::subtract(int, int)",
                               "Shape::area()",
                               "Shape::display_info()",
                               "Rectangle::Rectangle(double, double)",
                               "Rectangle::area()",
                               "Rectangle::display_info()",
                               "Circle::Circle(double)",
                               "Circle::area()",
                               "Circle::display_info()"]

class Requiri_Harness(unittest.TestCase):
    def setUp(self):
        test_directory = "test_files"
        project.set_code_location(test_directory)

        generate_test_cpp_file("test_files")
        self.list_of_signatures = list_of_function_signatures

    def tearDown(self):
        # Clean up test files after each test
        test_directory = "test_files"
        for file_name in os.listdir(test_directory):
            file_path = os.path.join(test_directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(test_directory)