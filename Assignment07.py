# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes with structured error handling
# Change Log: (Who, When, What)
#   RRoot, 1/1/2030, Created Script
#   ABelhumeur, 11/27/2023, Started Assignment 07
#   ABelhumeur, 11/28/2023, Editing Script and Final Testing
# ------------------------------------------------------------------------------------------ #

# Import Libraries
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # A table of student data
menu_choice: str  # Hold the choice made by the user.


# ---------- Inherited Data Classes ---------- #

class Person:
    """
    A Super / Parent class for storing data belonging to multiple persons, including first and last name.
    """

    def __init__(self, first_name: str = "", last_name: str = ""):
        """
        Define variables for the class "Person"
        """
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        """
        Gets first_name as an instanced variable.
        """
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        """
        Returns an error if first_name is set as anything but alphabetic characters.
        """
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("First name can only contain alphabetic characters.")

    @property
    def last_name(self):
        """
        Gets last_name as an instanced variable.
        """
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        """
        Returns an error if last_name is set as anything but alphabetic characters.
        """
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("Last name can only contain alphabetic characters.")

    def __str__(self):
        """
        :return: A string to return the instance of a Person's first and last name.
        """
        return f"{self.first_name} {self.last_name}"


class Student(Person):
    """
    A subclass of Person, Student stores data regarding the course name that a student is registered for, in
    addition to storing the student's first and last name inherited from Person.
    """

    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        """
        Define variables for the subclass, Student, and call existing variables from the super class, Person.
        """
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        """
        Gets course_name as an instanced variable.
        """
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        """
        Sets the value input for a course_name instance as a string.
        """
        self.__course_name = str(value)

    def __str__(self):
        """
        :return: A string to return the instance of Student, including inherited variables.
        """
        return f"{self.first_name} {self.last_name}, is enrolled in {self.course_name}"


# ---------- Processing Classes ---------- #

class FileProcessor:
    """
    A collection of processing layer functions that work with Json files.
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        This function reads JSON data from the specified file.
        :param file_name: A string indicating the specified file name.
        :param student_data: The roster of student data currently saved to the file.
        :return: Return the roster of student data currently saved to the file as a list.
        """
        dict_table: list[dict[str, str, str]] = []
        try:
            file = open(file_name, "r")
            dict_table = json.load(file)
        except FileNotFoundError as e:
            IO.output_error_messages(message="Text file not found", error=e)
            IO.output_error_messages(message="Creating file since it doesn't exist")
            file = open(file_name, 'w')
            json.dump(student_data, file)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if not file.closed:
                file.close()
        student_data: list[Student] = []
        for row in dict_table:
            first_name = row.get('FirstName', '')
            last_name = row.get('LastName', '')
            course_name = row.get('CourseName', '')
            student_data.append(Student(first_name, last_name, course_name))
        return student_data


    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        This function saves all entered data to the JSON file without erasing existing entries.
        :param file_name: A string indicating the specified file name.
        :param student_data: The roster of all student data entered.
        :return: Returns the roster of all student data.
        """
        try:
            file = open(file_name, "w")
            list_of_dictionary_data: list = []
            for student in student_data:
                student_json: dict = {
                    "FirstName": student.first_name,
                    "LastName": student.last_name,
                    "CourseName": student.course_name
                }
                list_of_dictionary_data.append(student_json)
            json.dump(list_of_dictionary_data, file, indent=1)
            print("All entries have been saved to the file 'Enrollments.json'.")
            file.close()
        except TypeError as e:
            IO.output_error_messages(message="Please check that the data is a valid JSON format", error=e)
        except Exception as e:
            IO.output_error_messages(message="There was a non-specific error!", error=e)
        finally:
            if not file.closed:
                file.close()
        return student_data


# ---------- Presentation Classes ---------- #

class IO:
    """
    A collection of presentation layer functions that manage user input and output
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        This function displays error messaging should an exception get called.
        :param message: Prints a string for custom error messaging or explaining how errors are addressed in
        the case of an exception.
        :param error: If there is an exception error, this parameter will print technical information.
        If there is no error, it will do nothing. By default, there is no error.
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def input_menu_choice(menu: str) -> str:
        """
        This function inputs the user's menu selection of either 1, 2, 3, or 4.
        :param menu: This variable is a string value that is the user's input.
        :return: Return the user's input.
        """
        global menu_choice
        menu_choice = input(menu)
        while menu_choice not in ['1', '2', '3', '4']:
            IO.output_error_messages(message="Please enter an option between 1 and 4")
            menu_choice = input(menu)
        return menu_choice

    @staticmethod
    def output_student_courses(student_data: list) -> None:
        """
        Displays all entered student data, showing the names of students and what course they are registered for.
        :param student_data: The roster of student data.
        :return: Returns nothing.
        """
        print("-" * 50)
        for student in student_data:
            if isinstance(student, Student):
                print(student)
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list) -> list:
        """
        Asks the user to input information required for each student, including the student's first name, last name,
        and the name of the course they're registering for, which all gets appended to student_data.
        :param student_data: The roster of all current student data.
        :return: Returns the roster of all student data.
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")
            new_student = Student(first_name=student_first_name, last_name=student_last_name, course_name=course_name)
            student_data.append(new_student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was an incorrect type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# ---------- Program: Present and Process Data ---------- #

# When the program starts, read the file data into a list of lists (table) and extract data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)
for student in students:
    print(student)

# Present and Process Data
while (True):

    # Present the menu of choices
    menu_choice = IO.input_menu_choice(MENU)

    # Input user data (Register a Student for a Course)
    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    # Show current data
    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        continue

    # Save data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Exit the Program (Stop the loop)
    elif menu_choice == "4":
        break
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
