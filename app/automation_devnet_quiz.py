# ─────────────────────────────────────────────────────────────────────────────
# Automation & DevNet quiz — add "ch-automation-devnet" to the QUIZZES dict
# in app/quizzes.py (see header there for the exact wiring).
# ─────────────────────────────────────────────────────────────────────────────

AUTOMATION_DEVNET_QUIZ = {
    "ch-automation-devnet": {
        "title": "Automation & DevNet Quiz: JSON/XML · Python · Orchestration · DNA Center",
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "question": "Why do most modern REST APIs (including Cisco DNA Center) use JSON over XML?",
                "options": [
                    "JSON is more secure",
                    "JSON is lighter weight and maps directly onto native data structures like dicts and lists",
                    "XML can't represent nested data",
                    "JSON requires no parsing",
                ],
                "answer": 1,
                "explanation": "JSON is leaner and converts straight into Python dicts/lists with json.loads() -- XML is heavier and shows up more in legacy/NETCONF systems.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "question": "Looping over a list of device dicts and catching exceptions per-device lets one unreachable device fail without crashing the whole automation run.",
                "answer": True,
                "explanation": "Wrapping each device's logic in its own try/except is exactly how production scripts keep going when device #37 out of 50 times out.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "question": "What's the difference between automation and orchestration?",
                "options": [
                    "They're the same thing",
                    "Automation does one task automatically; orchestration coordinates many automated tasks together, often in a specific order",
                    "Orchestration only applies to cloud platforms",
                    "Automation requires Ansible, orchestration doesn't",
                ],
                "answer": 1,
                "explanation": "Pushing one config change is automation. Chaining 'provision VLAN -> update firewall -> update DNS -> notify Slack' in order is orchestration.",
            },
            {
                "id": "q4",
                "type": "multiple_choice",
                "question": "In an Ansible playbook, what does the inventory define?",
                "options": [
                    "The exact commands to run",
                    "Which devices exist and how to connect to them",
                    "The YAML syntax rules",
                    "The rollback procedure",
                ],
                "answer": 1,
                "explanation": "The inventory lists devices/groups and connection details. The playbook then defines what to do to everything in that inventory.",
            },
            {
                "id": "q5",
                "type": "multiple_choice",
                "question": "Which of these is NOT one of Cisco DNA Center's four core workflow areas?",
                "options": ["Design", "Policy", "Provision", "Billing"],
                "answer": 3,
                "explanation": "The four are Design (network hierarchy), Policy (access rules), Provision (push config), and Assurance (health dashboards). Billing isn't one of them.",
            },
            {
                "id": "q6",
                "type": "true_false",
                "question": "The 'teach it back' study method is a good way to tell memorization apart from real understanding.",
                "answer": True,
                "explanation": "If you can explain a concept like ACLs to someone else in plain English, you understand it. If you can only recite the command, you memorized it.",
            },
        ],
    },
}
