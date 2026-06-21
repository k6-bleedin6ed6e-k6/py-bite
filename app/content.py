from .ooss_chapter import OOSS_CHAPTER
from .network_automation_chapter import NETWORK_AUTOMATION_CHAPTER
from .network_fundamentals_chapter import NETWORK_FUNDAMENTALS_CHAPTER
from .network_security_chapter import NETWORK_SECURITY_CHAPTER
from .automation_devnet_chapter import AUTOMATION_DEVNET_CHAPTER

CHAPTERS = [
    {
        "id": "ch1",
        "number": 1,
        "title": "Python Basics",
        "subtitle": "Variables, Strings, Numbers, Math & Comments",
        "description": "Start your Python journey with the fundamentals: how to store data in variables, work with text and numbers, perform calculations, and write clean code with comments.",
        "lessons": [
            {
                "id": "ch1_l1",
                "title": "Variables and Strings",
                "duration": "15 min",
                "objectives": [
                    "Understand what a variable is and how to name it",
                    "Create and manipulate string values",
                    "Use the print() function to output data"
                ],
                "sections": [
                    {
                        "heading": "What is a Variable?",
                        "body": "A variable is a named container that stores a value. In Python, you create a variable by assigning a value with the = operator.",
                        "code": 'name = "Alice"\nage = 30\nprint(name)\nprint(age)'
                    },
                    {
                        "heading": "Working with Strings",
                        "body": "Strings are text values surrounded by single or double quotes. You can combine strings with + and repeat them with *.",
                        "code": 'greeting = "Hello"\nname = "World"\nmessage = greeting + ", " + name + "!"\nprint(message)\nprint("Ha" * 3)'
                    },
                    {
                        "heading": "String Formatting with f-strings",
                        "body": "f-strings let you embed expressions inside string literals using curly braces.",
                        "code": 'first_name = "Ada"\nlast_name = "Lovelace"\nprint(f"My name is {first_name} {last_name}")'
                    },
                    {
                        "heading": "Course Example: Name Tag Generator",
                        "body": "This script from your course uses command-line arguments to build a simple name tag.",
                        "code": '"""\nThis module is a name tag generator.\n"""\nimport sys\n\nprint("*---------------------------------")\nprint("|", "First name: ", sys.argv[1])\nprint("|", "Second name: ", sys.argv[2])\nprint("*---------------------------------")',
                        "note": "When running this example, provide first and last names as arguments."
                    }
                ],
                "exercise": {
                    "title": "Create Your Own Bio",
                    "instruction": "Write a script that creates variables for your name, city, and hobby, then prints a sentence using an f-string.",
                    "starter_code": 'name = "Your Name"\ncity = "Your City"\nhobby = "Your Hobby"\n\n# Use an f-string to print your bio\nprint(f"My name is {name}. I live in {city} and I love {hobby}.")'
                }
            },
            {
                "id": "ch1_l2",
                "title": "Numbers and Math",
                "duration": "20 min",
                "objectives": [
                    "Use integers and floats",
                    "Perform arithmetic operations",
                    "Understand operator precedence",
                    "Write comments to document code"
                ],
                "sections": [
                    {
                        "heading": "Integers and Floats",
                        "body": "Python has two main numeric types: integers (whole numbers) and floats (decimal numbers).",
                        "code": "x = 10       # integer\ny = 3.14     # float\nprint(type(x))\nprint(type(y))"
                    },
                    {
                        "heading": "Arithmetic Operators",
                        "body": "Python supports standard math operators: +, -, *, /, // (floor division), % (modulo), and ** (exponent).",
                        "code": "a = 17\nb = 5\nprint(a + b)   # 22\nprint(a - b)   # 12\nprint(a * b)   # 85\nprint(a / b)   # 3.4\nprint(a // b)  # 3\nprint(a % b)   # 2\nprint(a ** b)  # 1419857"
                    },
                    {
                        "heading": "Course Example: Calculate Speed",
                        "body": "This example converts distance and time into multiple speed units using arithmetic.",
                        "code": "distance_in_km = 150\ntime_in_hours = 2\n\ndistance_in_mi = distance_in_km / 1.6\ndistance_in_mtrs = distance_in_km * 1000\n\ntime_in_seconds = time_in_hours * 3600\n\nspeed_in_kph = distance_in_km / time_in_hours\nspeed_in_mph = distance_in_mi / time_in_hours\nspeed_in_mps = distance_in_mtrs / time_in_seconds\n\nprint(\"The speed in kilometers per hour is:\", speed_in_kph)\nprint(\"The speed in miles per hour is:\", speed_in_mph)\nprint(\"The speed in meters per second is:\", speed_in_mps)"
                    },
                    {
                        "heading": "Course Example: Circle Calculations",
                        "body": "Using a constant and the exponent operator to compute circle properties.",
                        "code": "PI = 3.14159\nradius = 7\n\narea = PI * radius**2\ncircumference = 2 * PI * radius\n\nprint(\"Circumference of the circle:\", circumference)\nprint(\"Area of the circle:\", area)"
                    }
                ],
                "exercise": {
                    "title": "Temperature Converter",
                    "instruction": "Write a script that converts a Celsius temperature to Fahrenheit using the formula: F = (C × 9/5) + 32.",
                    "starter_code": "celsius = 25\n# Calculate Fahrenheit here\nfahrenheit = (celsius * 9/5) + 32\nprint(f\"{celsius}°C is {fahrenheit}°F\")"
                }
            },
            {
                "id": "ch1_l3",
                "title": "User Input and Type Conversion",
                "duration": "15 min",
                "objectives": [
                    "Capture user input with input()",
                    "Convert between data types",
                    "Handle basic input errors"
                ],
                "sections": [
                    {
                        "heading": "Getting Input from the User",
                        "body": "The input() function pauses your program and waits for the user to type something.",
                        "code": 'name = input("What is your name? ")\nprint(f"Hello, {name}!")'
                    },
                    {
                        "heading": "Converting Input to Numbers",
                        "body": "input() always returns a string. Use int() or float() to convert it for math.",
                        "code": 'age = int(input("Enter your age: "))\nprint(f"Next year you will be {age + 1}")'
                    },
                    {
                        "heading": "Course Example: Binary Converter",
                        "body": "A script that takes a decimal number and converts it to binary.",
                        "code": 'number = input("Convert to binary: ")\n\n# convert to integer\ninteger = int(number)\n\n# convert integer to binary\nbinary = bin(integer)\n\nprint(binary)'
                    },
                    {
                        "heading": "Course Example: Days Converter",
                        "body": "Break a total number of days into years, weeks, and remaining days.",
                        "code": "days = int(input(\"Number of days:\"))\n\nyears = days // 365\nweeks = (days % 365) // 7\ndays = days - ((years * 365) + (weeks * 7))\n\nprint(\"Years:\", years)\nprint(\"Weeks:\", weeks)\nprint(\"Days:\", days)"
                    }
                ],
                "exercise": {
                    "title": "Simple Calculator",
                    "instruction": "Ask the user for two numbers and print their sum, difference, product, and quotient.",
                    "starter_code": 'num1 = float(input("Enter first number: "))\nnum2 = float(input("Enter second number: "))\n\nprint(f"Sum: {num1 + num2}")\n# Add the remaining operations below\nprint(f"Difference: {num1 - num2}")\nprint(f"Product: {num1 * num2}")\nprint(f"Quotient: {num1 / num2}")'
                }
            }
        ]
    },
    {
        "id": "ch2",
        "number": 2,
        "title": "Control Flow",
        "subtitle": "Booleans, Conditionals & Loops",
        "description": "Learn how to make decisions in your code with if/else statements and automate repetition with for and while loops.",
        "lessons": [
            {
                "id": "ch2_l1",
                "title": "Booleans and Comparisons",
                "duration": "15 min",
                "objectives": [
                    "Understand True and False",
                    "Use comparison operators",
                    "Combine conditions with and, or, not"
                ],
                "sections": [
                    {
                        "heading": "Boolean Values",
                        "body": "Booleans represent truth values: True or False. They are the foundation of decision-making in code.",
                        "code": "is_raining = True\nhas_umbrella = False\nprint(type(is_raining))"
                    },
                    {
                        "heading": "Comparison Operators",
                        "body": "Use ==, !=, <, >, <=, >= to compare values and get a boolean result.",
                        "code": "x = 10\ny = 20\nprint(x == y)   # False\nprint(x != y)   # True\nprint(x < y)    # True\nprint(x >= 10)  # True"
                    },
                    {
                        "heading": "Logical Operators",
                        "body": "Combine comparisons with and, or, and not.",
                        "code": "age = 25\nhas_id = True\ncan_vote = age >= 18 and has_id\nprint(can_vote)\n\n# not flips the value\nprint(not False)"
                    }
                ],
                "exercise": {
                    "title": "Eligibility Checker",
                    "instruction": "Create variables for age and a boolean has_ticket. Print whether the person can enter (age >= 13 and has_ticket).",
                    "starter_code": "age = 15\nhas_ticket = True\ncan_enter = age >= 13 and has_ticket\nprint(f\"Can enter: {can_enter}\")"
                }
            },
            {
                "id": "ch2_l2",
                "title": "If, Elif, and Else",
                "duration": "20 min",
                "objectives": [
                    "Write conditional blocks with if",
                    "Chain conditions with elif",
                    "Provide fallback actions with else"
                ],
                "sections": [
                    {
                        "heading": "The if Statement",
                        "body": "An if statement runs a block of code only when its condition is True. Indentation matters in Python.",
                        "code": 'temperature = 85\nif temperature > 80:\n    print("It is hot outside!")\n    print("Stay hydrated.")'
                    },
                    {
                        "heading": "if / elif / else",
                        "body": "Use elif to check additional conditions, and else as a catch-all.",
                        "code": 'score = 78\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelif score >= 70:\n    print("C")\nelse:\n    print("D or F")'
                    },
                    {
                        "heading": "Course Example: True or False Quiz",
                        "body": "A simple quiz that checks user input and responds accordingly.",
                        "code": 'answer = input("Return TRUE or FALSE: Python was released in 1991:\\n")\n\nif answer == "TRUE":\n print(\'Correct\')\nelif answer == "FALSE":\n print(\'Wrong\')\nelif answer != ("TRUE" or "FALSE"):\n print(\'Please answer TRUE or FALSE\')\nprint(\'Bye!\')'
                    }
                ],
                "exercise": {
                    "title": "Number Classifier",
                    "instruction": "Write a script that takes a number and prints whether it is positive, negative, or zero.",
                    "starter_code": "num = int(input(\"Enter a number: \"))\nif num > 0:\n    print(\"Positive\")\nelif num < 0:\n    print(\"Negative\")\nelse:\n    print(\"Zero\")"
                }
            },
            {
                "id": "ch2_l3",
                "title": "For Loops",
                "duration": "20 min",
                "objectives": [
                    "Iterate over sequences with for",
                    "Use range() to generate number sequences",
                    "Control loop flow with break and continue"
                ],
                "sections": [
                    {
                        "heading": "Looping Over Sequences",
                        "body": "A for loop repeats a block of code for each item in a sequence.",
                        "code": 'fruits = ["apple", "banana", "cherry"]\nfor fruit in fruits:\n    print(fruit)'
                    },
                    {
                        "heading": "The range() Function",
                        "body": "range() generates a sequence of numbers. Use it when you need to repeat something a specific number of times.",
                        "code": "for i in range(5):\n    print(i)\n\n# range(start, stop, step)\nfor i in range(2, 11, 2):\n    print(i)"
                    },
                    {
                        "heading": "break and continue",
                        "body": "break exits the loop entirely. continue skips the rest of the current iteration.",
                        "code": "for num in range(10):\n    if num == 3:\n        continue\n    if num == 7:\n        break\n    print(num)"
                    },
                    {
                        "heading": "Course Example: Summing Even Numbers",
                        "body": "This script sums every even number from 2 to 100 using range with a step.",
                        "code": "total = 0\nfor number in range(2,101,2):\n total += number\nprint(total)"
                    },
                    {
                        "heading": "Course Example: Nested Loops",
                        "body": "You can place one loop inside another to work with combinations of values.",
                        "code": "for even in range(2,11,2):\n  for odd in range(1,11,2):\n    val = even + odd\n    print(even, \"+\", odd, \"=\", val)"
                    }
                ],
                "exercise": {
                    "title": "Multiplication Table",
                    "instruction": "Use a nested for loop to print a 5x5 multiplication table.",
                    "starter_code": "for i in range(1, 6):\n    for j in range(1, 6):\n        print(f\"{i*j:2}\", end=\" \")\n    print()"
                }
            },
            {
                "id": "ch2_l4",
                "title": "While Loops",
                "duration": "15 min",
                "objectives": [
                    "Repeat code while a condition is true",
                    "Avoid infinite loops",
                    "Build interactive programs"
                ],
                "sections": [
                    {
                        "heading": "Basic while Loop",
                        "body": "A while loop repeats as long as its condition remains True.",
                        "code": "count = 0\nwhile count < 5:\n    print(count)\n    count += 1"
                    },
                    {
                        "heading": "Course Example: Password Check",
                        "body": "Keep asking for a password until the correct one is entered.",
                        "code": 'user_pass = "random"\nvalid = False\nwhile not valid:\n password = input("please enter your password: ")\n if password == user_pass:\n   print("Welcome back user!")\n   valid = True\n else:\n   print("invalid password, try again... ")'
                    }
                ],
                "exercise": {
                    "title": "Countdown Timer",
                    "instruction": "Write a while loop that counts down from 10 to 1, then prints 'Blastoff!'.",
                    "starter_code": "count = 10\nwhile count > 0:\n    print(count)\n    count -= 1\nprint(\"Blastoff!\")"
                }
            }
        ]
    },
    {
        "id": "ch3",
        "number": 3,
        "title": "Functions",
        "subtitle": "Defining, Arguments & Lambda",
        "description": "Functions are reusable blocks of code. Learn to define your own, pass data in, and return results.",
        "lessons": [
            {
                "id": "ch3_l1",
                "title": "Defining and Calling Functions",
                "duration": "20 min",
                "objectives": [
                    "Define a function with def",
                    "Pass parameters and return values",
                    "Understand local vs global scope"
                ],
                "sections": [
                    {
                        "heading": "Creating a Function",
                        "body": "Use the def keyword followed by a name and parentheses. The indented block is the function body.",
                        "code": 'def greet(name):\n    message = f"Hello, {name}!"\n    return message\n\nresult = greet("Alice")\nprint(result)'
                    },
                    {
                        "heading": "Parameters and Return",
                        "body": "Functions can accept multiple inputs and return a single output.",
                        "code": 'def rectangle_area(width, height):\n    return width * height\n\narea = rectangle_area(5, 3)\nprint(f"Area: {area}")'
                    },
                    {
                        "heading": "Default Parameters",
                        "body": "You can provide default values for parameters.",
                        "code": 'def power(base, exponent=2):\n    return base ** exponent\n\nprint(power(3))      # 9\nprint(power(2, 3))   # 8'
                    }
                ],
                "exercise": {
                    "title": "Greeting Generator",
                    "instruction": "Write a function called greet that takes a name and a greeting ('Hello' by default) and returns the full greeting string.",
                    "starter_code": 'def greet(name, greeting="Hello"):\n    return f"{greeting}, {name}!"\n\nprint(greet("Alice"))\nprint(greet("Bob", "Hi"))'
                }
            },
            {
                "id": "ch3_l2",
                "title": "Variable Arguments",
                "duration": "15 min",
                "objectives": [
                    "Accept any number of positional arguments with *args",
                    "Accept any number of keyword arguments with **kwargs",
                    "Unpack arguments when calling functions"
                ],
                "sections": [
                    {
                        "heading": "*args for Positional Arguments",
                        "body": "Use *args to accept any number of positional arguments as a tuple.",
                        "code": "def total(*numbers):\n    result = 0\n    for n in numbers:\n        result += n\n    return result\n\nprint(total(1, 2, 3))\nprint(total(10, 20))"
                    },
                    {
                        "heading": "Course Example: Filtering Arguments",
                        "body": "This function prints only non-integer arguments passed to it.",
                        "code": "def print_arguments(*args):\n  for value in args:\n    if type(value) == int:\n      continue\n    print(value)\n\nprint_arguments(1, \"hello\", 2, \"world\", 3.14)"
                    }
                ],
                "exercise": {
                    "title": "Flexible Average",
                    "instruction": "Write a function average(*numbers) that returns the average of all provided numbers.",
                    "starter_code": "def average(*numbers):\n    if not numbers:\n        return 0\n    return sum(numbers) / len(numbers)\n\nprint(average(10, 20, 30))\nprint(average(5, 15))"
                }
            },
            {
                "id": "ch3_l3",
                "title": "Lambda Functions",
                "duration": "15 min",
                "objectives": [
                    "Write small anonymous functions with lambda",
                    "Use lambda with map, filter, and sorted"
                ],
                "sections": [
                    {
                        "heading": "Lambda Syntax",
                        "body": "A lambda is a small, unnamed function defined in a single line.",
                        "code": "square = lambda x: x ** 2\nprint(square(5))"
                    },
                    {
                        "heading": "Course Example: Power Lambda",
                        "body": "A lambda that calculates a number raised to a given power.",
                        "code": "answer = lambda number, power : number ** power\n\nprint(answer(2, 3))\nprint(answer(5, 2))"
                    },
                    {
                        "heading": "Using Lambda with Built-ins",
                        "body": "Lambdas shine when used as short callbacks.",
                        "code": 'names = ["Alice", "bob", "Charlie", "diana"]\nnames.sort(key=lambda n: n.lower())\nprint(names)'
                    }
                ],
                "exercise": {
                    "title": "Lambda Filter",
                    "instruction": "Use filter() with a lambda to get only the even numbers from the list.",
                    "starter_code": "numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nevens = list(filter(lambda x: x % 2 == 0, numbers))\nprint(evens)"
                }
            }
        ]
    },
    {
        "id": "ch4",
        "number": 4,
        "title": "Collections",
        "subtitle": "Lists, Tuples, Dictionaries & Sets",
        "description": "Master Python's built-in data structures for organizing and manipulating groups of data.",
        "lessons": [
            {
                "id": "ch4_l1",
                "title": "Lists",
                "duration": "25 min",
                "objectives": [
                    "Create and modify lists",
                    "Use indexing and slicing",
                    "Apply common list methods"
                ],
                "sections": [
                    {
                        "heading": "Creating Lists",
                        "body": "A list is an ordered, mutable collection of items.",
                        "code": 'fruits = ["apple", "banana", "cherry"]\nmixed = [1, "two", 3.0, True]\nprint(fruits[0])   # first item\nprint(fruits[-1])  # last item'
                    },
                    {
                        "heading": "List Methods",
                        "body": "Lists have powerful built-in methods for manipulation.",
                        "code": 'animals = []\nanimals.append("Lion")\nanimals.append("Zebra")\nanimals.insert(1, "Elephant")\nanimals.remove("Zebra")\nprint(animals)\nprint(len(animals))'
                    },
                    {
                        "heading": "Slicing",
                        "body": "Extract portions of a list with start:stop:step syntax.",
                        "code": "nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\nprint(nums[2:5])\nprint(nums[:3])\nprint(nums[::2])\nprint(nums[::-1])"
                    },
                    {
                        "heading": "Course Example: List Operations",
                        "body": "A walkthrough of common list operations from your course.",
                        "code": 'wild = ["Lion", "Zebra", "Panther", "Antelope"]\nwild.append("Elephant")\nanimals = []\nanimals.extend(wild)\nanimals.insert(2, "Cheetah")\nanimals.pop(1)\nanimals.insert(1, "Giraffe")\nanimals.sort(key=None, reverse=False)\nprint(animals)'
                    }
                ],
                "exercise": {
                    "title": "Shopping List Manager",
                    "instruction": "Create a shopping list, add three items, remove one, sort it, and print the result.",
                    "starter_code": 'shopping = []\nshopping.append("Milk")\nshopping.append("Eggs")\nshopping.append("Bread")\nshopping.remove("Eggs")\nshopping.sort()\nprint(shopping)'
                }
            },
            {
                "id": "ch4_l2",
                "title": "Tuples",
                "duration": "15 min",
                "objectives": [
                    "Understand immutable sequences",
                    "Use tuples for fixed data",
                    "Unpack tuples into variables"
                ],
                "sections": [
                    {
                        "heading": "Tuple Basics",
                        "body": "Tuples are like lists but immutable. Once created, they cannot be changed.",
                        "code": 'point = (10, 20)\nprint(point[0])\n# point[0] = 15  # This would raise an error'
                    },
                    {
                        "heading": "Tuple Unpacking",
                        "body": "Assign tuple elements directly to variables.",
                        "code": "coords = (3, 4)\nx, y = coords\nprint(x, y)"
                    },
                    {
                        "heading": "Course Example: Pet Analysis",
                        "body": "Using tuple methods to analyze data.",
                        "code": 'pets = ("cat", "cat", "cat", "dog", "horse")\nc = pets.count("cat")\nd = len(pets)\nif (c/d)*100 > 50.0:\n  print("There are too many cats here")\nelse:\n  print("Everything is good")'
                    }
                ],
                "exercise": {
                    "title": "Coordinate Swap",
                    "instruction": "Create a tuple with two numbers. Use unpacking to swap their values and print both.",
                    "starter_code": "coords = (5, 10)\nx, y = coords\nprint(f\"Before: x={x}, y={y}\")\nx, y = y, x\nprint(f\"After: x={x}, y={y}\")"
                }
            },
            {
                "id": "ch4_l3",
                "title": "Dictionaries",
                "duration": "25 min",
                "objectives": [
                    "Store key-value pairs",
                    "Access, add, and remove items",
                    "Iterate over dictionaries"
                ],
                "sections": [
                    {
                        "heading": "Creating Dictionaries",
                        "body": "Dictionaries store data as key-value pairs for fast lookup.",
                        "code": 'person = {\n    "name": "Alice",\n    "age": 30,\n    "city": "New York"\n}\nprint(person["name"])'
                    },
                    {
                        "heading": "Modifying Dictionaries",
                        "body": "Add, update, and remove keys easily.",
                        "code": 'person = {"name": "Alice", "age": 30}\nperson["age"] = 31\nperson["job"] = "Engineer"\ndel person["age"]\nprint(person)'
                    },
                    {
                        "heading": "Course Example: Dictionary Masher",
                        "body": "Merge two dictionaries, keeping only new keys from the second.",
                        "code": "def dictionary_masher(dict_a, dict_b):\n  for key, value in dict_b.items():\n    if key not in dict_a:\n      dict_a[key] = value\n  return dict_a\n\na = {\"x\": 1, \"y\": 2}\nb = {\"y\": 99, \"z\": 3}\nprint(dictionary_masher(a, b))"
                    },
                    {
                        "heading": "Course Example: Sentence Analyzer",
                        "body": "Count the occurrences of each character in a sentence.",
                        "code": "def sentence_analyzer(sentence):\n  solution = {}\n  for char in sentence:\n    if char is not ' ':\n      if char in solution:\n        solution[char] += 1\n      else:\n        solution[char] = 1\n  return solution\n\nprint(sentence_analyzer(\"hello world\"))"
                    }
                ],
                "exercise": {
                    "title": "Phone Book",
                    "instruction": "Create a dictionary with three names and phone numbers. Write a function lookup(name) that returns the number or 'Not found'.",
                    "starter_code": 'phone_book = {\n    "Alice": "555-1234",\n    "Bob": "555-5678",\n    "Charlie": "555-9999"\n}\n\ndef lookup(name):\n    return phone_book.get(name, "Not found")\n\nprint(lookup("Alice"))\nprint(lookup("Dave"))'
                }
            },
            {
                "id": "ch4_l4",
                "title": "Sets",
                "duration": "15 min",
                "objectives": [
                    "Create unordered collections of unique items",
                    "Perform set operations: union, intersection, difference",
                    "Remove duplicates from data"
                ],
                "sections": [
                    {
                        "heading": "Set Basics",
                        "body": "Sets are unordered collections with no duplicates.",
                        "code": 'numbers = {1, 2, 3, 3, 3}\nprint(numbers)\nnumbers.add(4)\nnumbers.remove(2)\nprint(numbers)'
                    },
                    {
                        "heading": "Set Operations",
                        "body": "Perform mathematical set operations.",
                        "code": "a = {1, 2, 3, 4}\nb = {3, 4, 5, 6}\nprint(a | b)   # union\nprint(a & b)   # intersection\nprint(a - b)   # difference"
                    },
                    {
                        "heading": "Course Example: Set Maker",
                        "body": "Convert a list to a set to remove duplicates.",
                        "code": "def set_maker(the_list):\n  return set(the_list)\n\nprint(set_maker([1, 2, 2, 3, 3, 3]))"
                    },
                    {
                        "heading": "Course Example: Find Union",
                        "body": "Manually compute the union of two lists without duplicates.",
                        "code": "def find_union(list_a, list_b):\n  union = []\n  for element in list_a + list_b:\n    if element not in union:\n      union.append(element)\n  return union\n\nprint(find_union([1, 2, 3], [2, 3, 4]))"
                    }
                ],
                "exercise": {
                    "title": "Unique Words",
                    "instruction": "Split a sentence into words and create a set of unique words.",
                    "starter_code": 'sentence = "the quick brown fox jumps over the lazy dog"\nwords = sentence.split()\nunique = set(words)\nprint(f"Total words: {len(words)}")\nprint(f"Unique words: {len(unique)}")\nprint(unique)'
                }
            }
        ]
    },
    {
        "id": "ch5",
        "number": 5,
        "title": "Advanced Python",
        "subtitle": "OOP, Files, Error Handling & Modules",
        "description": "Level up with object-oriented programming, file I/O, exception handling, and organizing code into modules.",
        "lessons": [
            {
                "id": "ch5_l1",
                "title": "Object-Oriented Programming",
                "duration": "30 min",
                "objectives": [
                    "Define classes and create objects",
                    "Use __init__ and self",
                    "Understand inheritance"
                ],
                "sections": [
                    {
                        "heading": "Creating a Class",
                        "body": "A class is a blueprint for objects. Use __init__ to set up initial state.",
                        "code": "class Dog:\n    def __init__(self, name, breed):\n        self.name = name\n        self.breed = breed\n\n    def bark(self):\n        return f\"{self.name} says woof!\"\n\nbuddy = Dog(\"Buddy\", \"Golden Retriever\")\nprint(buddy.bark())"
                    },
                    {
                        "heading": "Class Attributes",
                        "body": "Attributes shared across all instances of a class.",
                        "code": "class Elevator:\n    occupancy_limit = 8\n\n    def __init__(self, occupants):\n        if occupants > self.occupancy_limit:\n            print(f\"Limit exceeded. {occupants - self.occupancy_limit} must exit.\")\n        self.occupants = occupants\n\ne1 = Elevator(6)\ne2 = Elevator(10)\nprint(e1.occupants, e2.occupants)"
                    },
                    {
                        "heading": "Course Example: CameraPhone (Multiple Inheritance)",
                        "body": "A class can inherit from more than one parent.",
                        "code": "class MobilePhone:\n    def __init__(self, memory):\n        self.memory = memory\n\nclass Camera:\n    def take_picture(self):\n        print(\"Say cheese!\")\n\nclass CameraPhone(MobilePhone, Camera):\n    pass\n\ncp = CameraPhone(\"200KB\")\ncp.take_picture()\nprint(cp.memory)"
                    },
                    {
                        "heading": "Course Example: Circle Class",
                        "body": "A class that calculates geometric properties.",
                        "code": "import math\n\nclass Circle:\n    def __init__(self, radius):\n        self.radius = radius\n\n    def area(self):\n        return math.pi * self.radius ** 2\n\n    def circumference(self):\n        return 2 * math.pi * self.radius\n\n    def change_radius(self, new_radius):\n        self.radius = new_radius\n\nc = Circle(7)\nprint(c.area())\nc.change_radius(10)\nprint(c.area())"
                    }
                ],
                "exercise": {
                    "title": "Bank Account",
                    "instruction": "Create a BankAccount class with deposit, withdraw, and get_balance methods.",
                    "starter_code": "class BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.balance = balance\n\n    def deposit(self, amount):\n        self.balance += amount\n        return self.balance\n\n    def withdraw(self, amount):\n        if amount > self.balance:\n            return \"Insufficient funds\"\n        self.balance -= amount\n        return self.balance\n\nacc = BankAccount(\"Alice\", 100)\nprint(acc.deposit(50))\nprint(acc.withdraw(30))\nprint(acc.withdraw(200))"
                }
            },
            {
                "id": "ch5_l2",
                "title": "Working with Files",
                "duration": "20 min",
                "objectives": [
                    "Open, read, and write text files",
                    "Use with statements for safe file handling",
                    "Process CSV data"
                ],
                "sections": [
                    {
                        "heading": "Reading a File",
                        "body": "Use open() with mode 'r' to read. The with statement ensures the file closes automatically.",
                        "code": 'with open("example.txt", "r") as f:\n    content = f.read()\n    print(content)'
                    },
                    {
                        "heading": "Writing a File",
                        "body": "Use mode 'w' to overwrite or 'a' to append.",
                        "code": 'with open("output.txt", "w") as f:\n    f.write("Hello, file!\\n")\n    f.write("Second line\\n")'
                    },
                    {
                        "heading": "Reading Line by Line",
                        "body": "Iterate over a file object to process one line at a time.",
                        "code": 'with open("data.txt", "r") as f:\n    for line in f:\n        print(line.strip())'
                    },
                    {
                        "heading": "Course Example: Wage Calculator",
                        "body": "Read a CSV, process wages, and write results to a new file.",
                        "code": "import csv\n\n# Simulated in-memory processing\nimport io\ninput_csv = \"name,hours\\nAlice,8\\nBob,10\"\n\noutput_data = []\nreader = csv.reader(io.StringIO(input_csv))\nnext(reader)  # skip header\nfor row in reader:\n    row[1] = int(row[1]) * 15\n    output_data.append(row)\n\nprint(output_data)"
                    }
                ],
                "exercise": {
                    "title": "Write a Poem",
                    "instruction": "Write a list of lines to a file called poem.txt, then read it back and print it.",
                    "starter_code": 'lines = ["Roses are red,", "Violets are blue,", "Python is awesome,", "And so are you."]\n\nwith open("poem.txt", "w") as f:\n    for line in lines:\n        f.write(line + "\\n")\n\nwith open("poem.txt", "r") as f:\n    print(f.read())'
                }
            },
            {
                "id": "ch5_l3",
                "title": "Error Handling",
                "duration": "20 min",
                "objectives": [
                    "Catch exceptions with try/except",
                    "Handle specific error types",
                    "Use finally for cleanup",
                    "Create custom exceptions"
                ],
                "sections": [
                    {
                        "heading": "Try and Except",
                        "body": "Wrap risky code in a try block and handle errors in except.",
                        "code": 'try:\n    num = int(input("Enter a number: "))\n    print(10 / num)\nexcept ValueError:\n    print("That was not a valid number.")\nexcept ZeroDivisionError:\n    print("Cannot divide by zero.")'
                    },
                    {
                        "heading": "Else and Finally",
                        "body": "else runs if no exception occurs. finally always runs.",
                        "code": "try:\n    result = 10 / 2\nexcept ZeroDivisionError:\n    print(\"Error\")\nelse:\n    print(f\"Result: {result}\")\nfinally:\n    print(\"Cleanup complete.\")"
                    },
                    {
                        "heading": "Course Example: File Error Handling",
                        "body": "Robust file reading with multiple exception types.",
                        "code": "try:\n    with open('input.txt', 'r') as f:\n        for line in f:\n            print(line)\nexcept FileNotFoundError:\n    print(\"Whoops! File does not exist.\")\nexcept Exception:\n    print(\"Something unforeseen happened\")\nfinally:\n    print(\"I will always show up\")"
                    },
                    {
                        "heading": "Course Example: Custom Exception",
                        "body": "Define your own exception by inheriting from Exception.",
                        "code": "class RecipeNotValidError(Exception):\n    def __init__(self):\n        self.message = \"Your recipe is not valid\"\n\ntry:\n    raise RecipeNotValidError\nexcept RecipeNotValidError as e:\n    print(e.message)"
                    }
                ],
                "exercise": {
                    "title": "Safe Division",
                    "instruction": "Write a function safe_divide(a, b) that returns the result or an error message, handling ZeroDivisionError and TypeError.",
                    "starter_code": "def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return \"Cannot divide by zero\"\n    except TypeError:\n        return \"Invalid types\"\n\nprint(safe_divide(10, 2))\nprint(safe_divide(10, 0))\nprint(safe_divide(10, \"a\"))"
                }
            },
            {
                "id": "ch5_l4",
                "title": "Modules and Packages",
                "duration": "15 min",
                "objectives": [
                    "Import built-in and custom modules",
                    "Use from...import syntax",
                    "Explore module contents with dir()"
                ],
                "sections": [
                    {
                        "heading": "Importing Modules",
                        "body": "Use import to bring in code from other files or the standard library.",
                        "code": "import math\nprint(math.pi)\nprint(math.sqrt(16))"
                    },
                    {
                        "heading": "Selective Imports",
                        "body": "Import only what you need to keep namespaces clean.",
                        "code": "from random import randint, choice\nprint(randint(1, 6))\nprint(choice([\"apple\", \"banana\", \"cherry\"]))"
                    },
                    {
                        "heading": "Course Example: Package Enumerator",
                        "body": "List all resources defined in a module using dir().",
                        "code": "import math\n\nresources = dir(math)\nfor resource in resources:\n    print(resource)"
                    }
                ],
                "exercise": {
                    "title": "Date Formatter",
                    "instruction": "Import datetime and print the current date in YYYY-MM-DD format.",
                    "starter_code": "from datetime import datetime\n\nnow = datetime.now()\nprint(now.strftime(\"%Y-%m-%d\"))"
                }
            }
        ]
    },
    OOSS_CHAPTER,
    NETWORK_AUTOMATION_CHAPTER,
    NETWORK_FUNDAMENTALS_CHAPTER,
    NETWORK_SECURITY_CHAPTER,
    AUTOMATION_DEVNET_CHAPTER,
]


def get_chapter(chapter_id):
    for ch in CHAPTERS:
        if ch["id"] == chapter_id:
            return ch
    return None


def get_lesson(lesson_id):
    for ch in CHAPTERS:
        for lesson in ch["lessons"]:
            if lesson["id"] == lesson_id:
                return lesson, ch
    return None, None
