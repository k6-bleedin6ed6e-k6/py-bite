from .ooss_quiz import OOSS_QUIZ
from .network_automation_quiz import NETWORK_AUTOMATION_QUIZ
from .network_fundamentals_quiz import NETWORK_FUNDAMENTALS_QUIZ
from .network_security_quiz import NETWORK_SECURITY_QUIZ
from .automation_devnet_quiz import AUTOMATION_DEVNET_QUIZ

QUIZZES = {
    "ch1": {
        "title": "Chapter 1 Quiz: Python Basics",
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "question": "Which of the following is a valid variable name in Python?",
                "options": ["2nd_value", "_hidden", "class", "my-variable"],
                "answer": 1,
                "explanation": "Variable names cannot start with a number, cannot be reserved keywords like 'class', and cannot contain hyphens. '_hidden' is valid."
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "question": "What is the output of print(\"Hello\" + \" \" + \"World\")?",
                "options": ["HelloWorld", "Hello World", "Hello+World", "Error"],
                "answer": 1,
                "explanation": "The + operator concatenates strings, and the space string \" \" adds a space between them."
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "question": "What does the // operator do?",
                "options": ["Division", "Floor division", "Exponentiation", "Modulo"],
                "answer": 1,
                "explanation": "// performs floor division, returning the largest whole number less than or equal to the result."
            },
            {
                "id": "q4",
                "type": "true_false",
                "question": "The input() function always returns a string.",
                "answer": True,
                "explanation": "input() captures text from the user and returns it as a string, even if digits are entered."
            },
            {
                "id": "q5",
                "type": "multiple_choice",
                "question": "Which function converts a string to an integer?",
                "options": ["str()", "int()", "float()", "bool()"],
                "answer": 1,
                "explanation": "int() converts a compatible value to an integer."
            }
        ]
    },
    "ch2": {
        "title": "Chapter 2 Quiz: Control Flow",
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "question": "What is the result of 5 > 3 and 2 < 1?",
                "options": ["True", "False", "Error", "None"],
                "answer": 1,
                "explanation": "5 > 3 is True, but 2 < 1 is False. True and False evaluates to False."
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "question": "How many times will this loop run? for i in range(3):",
                "options": ["2", "3", "4", "Infinite"],
                "answer": 1,
                "explanation": "range(3) generates 0, 1, 2 — three values, so the loop runs three times."
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "question": "What does the 'break' keyword do inside a loop?",
                "options": [
                    "Skips the current iteration",
                    "Exits the loop entirely",
                    "Restarts the loop",
                    "Does nothing"
                ],
                "answer": 1,
                "explanation": "break immediately terminates the innermost loop it is placed in."
            },
            {
                "id": "q4",
                "type": "true_false",
                "question": "An elif block requires a matching if before it.",
                "answer": True,
                "explanation": "elif (else if) is only valid when it follows an if statement."
            },
            {
                "id": "q5",
                "type": "multiple_choice",
                "question": "Which loop is best when the number of iterations is unknown?",
                "options": ["for", "while", "if", "def"],
                "answer": 1,
                "explanation": "A while loop continues until a condition is met, making it ideal when iterations depend on runtime conditions."
            }
        ]
    },
    "ch3": {
        "title": "Chapter 3 Quiz: Functions",
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "question": "What keyword is used to define a function?",
                "options": ["func", "function", "def", "define"],
                "answer": 2,
                "explanation": "Python uses the def keyword to define functions."
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "question": "What does *args collect inside a function?",
                "options": [
                    "Keyword arguments",
                    "Positional arguments as a tuple",
                    "Return values",
                    "Global variables"
                ],
                "answer": 1,
                "explanation": "*args gathers all extra positional arguments into a tuple."
            },
            {
                "id": "q3",
                "type": "true_false",
                "question": "A lambda function can contain multiple statements.",
                "answer": False,
                "explanation": "Lambdas are limited to a single expression; they cannot contain statements like assignments or loops."
            },
            {
                "id": "q4",
                "type": "multiple_choice",
                "question": "What happens if a function has no return statement?",
                "options": ["It raises an error", "It returns None", "It returns 0", "It returns True"],
                "answer": 1,
                "explanation": "Functions without an explicit return statement return None by default."
            },
            {
                "id": "q5",
                "type": "multiple_choice",
                "question": "Which of the following is a valid lambda?",
                "options": [
                    "lambda x: return x + 1",
                    "lambda x: x + 1",
                    "def lambda x: x + 1",
                    "lambda (x): x + 1"
                ],
                "answer": 1,
                "explanation": "lambda x: x + 1 is correct. The return keyword is implicit, and parentheses around the parameter are not used."
            }
        ]
    },
    "ch4": {
        "title": "Chapter 4 Quiz: Collections",
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "question": "Which collection type is immutable?",
                "options": ["list", "dict", "set", "tuple"],
                "answer": 3,
                "explanation": "Tuples cannot be changed after creation, making them immutable."
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "question": "How do you add an item to the end of a list?",
                "options": ["add()", "push()", "append()", "insert()"],
                "answer": 2,
                "explanation": "list.append(item) adds an item to the end of the list."
            },
            {
                "id": "q3",
                "type": "true_false",
                "question": "A dictionary stores items in key-value pairs.",
                "answer": True,
                "explanation": "Dictionaries map unique keys to values for fast lookup."
            },
            {
                "id": "q4",
                "type": "multiple_choice",
                "question": "What will len({1, 2, 2, 3}) return?",
                "options": ["2", "3", "4", "Error"],
                "answer": 1,
                "explanation": "Sets remove duplicates, so {1, 2, 2, 3} becomes {1, 2, 3}, which has a length of 3."
            },
            {
                "id": "q5",
                "type": "multiple_choice",
                "question": "Which method returns the value for a key, or a default if the key is missing?",
                "options": ["keys()", "values()", "get()", "items()"],
                "answer": 2,
                "explanation": "dict.get(key, default) safely retrieves values without raising KeyError."
            }
        ]
    },
    "ch5": {
        "title": "Chapter 5 Quiz: Advanced Python",
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "question": "What is the purpose of __init__ in a class?",
                "options": [
                    "To delete the object",
                    "To initialize the object's attributes",
                    "To print the object",
                    "To define class methods"
                ],
                "answer": 1,
                "explanation": "__init__ is the constructor method called when a new object is created."
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "question": "Which keyword is used to handle exceptions?",
                "options": ["handle", "catch", "except", "error"],
                "answer": 2,
                "explanation": "The except keyword catches exceptions raised in the matching try block."
            },
            {
                "id": "q3",
                "type": "true_false",
                "question": "The with statement automatically closes a file after use.",
                "answer": True,
                "explanation": "with creates a context manager that ensures cleanup (like closing a file) happens automatically."
            },
            {
                "id": "q4",
                "type": "multiple_choice",
                "question": "What does the finally block do?",
                "options": [
                    "Runs only if an exception occurs",
                    "Runs only if no exception occurs",
                    "Runs regardless of exceptions",
                    "Skips exceptions"
                ],
                "answer": 2,
                "explanation": "The finally block always executes, making it ideal for cleanup code."
            },
            {
                "id": "q5",
                "type": "multiple_choice",
                "question": "How do you import only the sqrt function from the math module?",
                "options": [
                    "import math.sqrt",
                    "from math import sqrt",
                    "import sqrt from math",
                    "include math.sqrt"
                ],
                "answer": 1,
                "explanation": "from math import sqrt brings only sqrt into the current namespace."
            }
        ]
    },
    **OOSS_QUIZ,
    **NETWORK_AUTOMATION_QUIZ,
    **NETWORK_FUNDAMENTALS_QUIZ,
    **NETWORK_SECURITY_QUIZ,
    **AUTOMATION_DEVNET_QUIZ,
}


def get_quiz(chapter_id):
    return QUIZZES.get(chapter_id)
