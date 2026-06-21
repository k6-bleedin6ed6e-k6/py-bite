# ─────────────────────────────────────────────────────────────────────────────
# Network Security quiz — add "ch-network-security" to the QUIZZES dict in
# app/quizzes.py (see header there for the exact wiring).
# ─────────────────────────────────────────────────────────────────────────────

NETWORK_SECURITY_QUIZ = {
    "ch-network-security": {
        "title": "Network Security Quiz: Hardening · Passwords · ACLs · Wi-Fi",
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "question": "Why should Telnet be replaced with SSH for remote management?",
                "options": [
                    "Telnet is slower",
                    "Telnet sends credentials and commands as plain unencrypted text",
                    "Telnet only works locally",
                    "Telnet requires a paid license",
                ],
                "answer": 1,
                "explanation": "Anyone capturing Telnet traffic can read usernames, passwords, and commands directly -- SSH encrypts the whole session.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "question": "`enable secret` is more secure than `enable password` because it hashes the password instead of storing it in reversible form.",
                "answer": True,
                "explanation": "enable password is essentially plaintext-reversible in the config file; enable secret applies a one-way hash.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "question": "What's the difference between a standard and an extended ACL?",
                "options": [
                    "Standard ACLs only filter by source IP; extended ACLs can also filter by destination, protocol, and port",
                    "Extended ACLs can only deny traffic, never permit it",
                    "Standard ACLs work on switches, extended ACLs work on routers",
                    "There's no real difference",
                ],
                "answer": 0,
                "explanation": "Standard ACLs are coarse (source IP only). Extended ACLs let you be precise -- e.g. allow only HTTPS traffic from a specific subnet.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "question": "Every Cisco ACL has an implicit 'deny all' at the very end, even if you never typed it.",
                "answer": True,
                "explanation": "Anything not explicitly permitted gets dropped by the invisible final rule -- a very common beginner gotcha.",
            },
            {
                "id": "q5",
                "type": "multiple_choice",
                "question": "Which Wi-Fi security setting should you avoid in production?",
                "options": ["WPA3", "WPA2-AES", "WEP", "802.1X with RADIUS"],
                "answer": 2,
                "explanation": "WEP is fundamentally broken and crackable in minutes -- never use it. WPA-TKIP is also weak; WPA2-AES or WPA3 are the floor for production.",
            },
            {
                "id": "q6",
                "type": "multiple_choice",
                "question": "Why should WPS be disabled on access points?",
                "options": [
                    "It slows down the network",
                    "It's trivially brute-forced, undermining otherwise strong Wi-Fi security",
                    "It only works with WEP",
                    "It's required for guest networks",
                ],
                "answer": 1,
                "explanation": "WPS's PIN-based pairing has well-known brute-force weaknesses that can expose the network even if WPA2/WPA3 is configured correctly.",
            },
        ],
    },
}
