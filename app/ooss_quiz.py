# ─────────────────────────────────────────────────────────────────────────────
# O-O/S-S quiz — add "ch6" to the QUIZZES dict in app/quizzes.py
# ─────────────────────────────────────────────────────────────────────────────

OOSS_QUIZ = {
    "ch6": {
        "title": "O-O/S-S Quiz: Object-Oriented Security Scripting",
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "question": "Which Python method runs automatically when you create a new object?",
                "options": ["__start__", "__create__", "__init__", "__new__"],
                "answer": 2,
                "explanation": "__init__ is the constructor. It runs the moment you call ClassName(), letting you set up the object's initial attributes.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "question": "A recursive function without a base case will:",
                "options": [
                    "Return None",
                    "Run once and stop",
                    "Crash with RecursionError",
                    "Loop forever without error",
                ],
                "answer": 2,
                "explanation": "Python enforces a recursion limit (default 1000). Without a base case the function keeps calling itself until Python raises RecursionError: maximum recursion depth exceeded.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "question": "socket.connect_ex() returns 0 when:",
                "options": [
                    "The port is closed",
                    "The host is unreachable",
                    "The port is open",
                    "A timeout occurs",
                ],
                "answer": 2,
                "explanation": "connect_ex() returns 0 on success (port open/accepting connections). Any non-zero return value indicates failure — closed, filtered, or unreachable.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "question": "Binary search requires the list to be sorted before it can work correctly.",
                "answer": True,
                "explanation": "Binary search works by comparing the target to the middle element and discarding half the list. This only works on a sorted list — otherwise the discard logic is wrong.",
            },
            {
                "id": "q5",
                "type": "multiple_choice",
                "question": "Which module helps count how many times each IP appears in a list of log entries?",
                "options": ["os", "socket", "collections.Counter", "re"],
                "answer": 2,
                "explanation": "Counter(list) counts occurrences of each unique value and counter.most_common() returns them ranked highest to lowest — perfect for finding top brute-force sources.",
            },
            {
                "id": "q6",
                "type": "multiple_choice",
                "question": "In OOP inheritance, class WebScanner(Scanner): means:",
                "options": [
                    "WebScanner replaces Scanner",
                    "WebScanner gets all of Scanner's methods and attributes",
                    "Scanner inherits from WebScanner",
                    "Both classes are independent",
                ],
                "answer": 1,
                "explanation": "The child class (WebScanner) inherits everything from the parent (Scanner). It can use parent methods directly and add new ones on top.",
            },
            {
                "id": "q7",
                "type": "true_false",
                "question": "Recursive directory scanning is useful in cybersecurity because malware often hides in deeply nested folders.",
                "answer": True,
                "explanation": "Recursion handles arbitrary depth without knowing how deep the tree goes in advance — making it the natural fit for directory scanning in forensic and antivirus tools.",
            },
            {
                "id": "q8",
                "type": "multiple_choice",
                "question": "What is the advantage of recursion over iteration for directory scanning?",
                "options": [
                    "It uses less memory",
                    "It is always faster",
                    "The code naturally mirrors the tree structure and handles any depth",
                    "It avoids PermissionError",
                ],
                "answer": 2,
                "explanation": "Recursive code reflects the tree structure directly — each call handles one level and delegates deeper levels to itself. The disadvantage is stack memory usage for very deep trees.",
            },
        ],
    }
}
