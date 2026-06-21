# ─────────────────────────────────────────────────────────────────────────────
# Network Fundamentals quiz — add "ch-network-fundamentals" to the QUIZZES
# dict in app/quizzes.py (see header there for the exact wiring).
# ─────────────────────────────────────────────────────────────────────────────

NETWORK_FUNDAMENTALS_QUIZ = {
    "ch-network-fundamentals": {
        "title": "Network Fundamentals Quiz: Managing Networks · Commands · SNMP · NetFlow · IP SLA",
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "question": "Which FCAPS category covers keeping the network fast?",
                "options": ["Fault", "Configuration", "Performance", "Accounting"],
                "answer": 2,
                "explanation": "Performance management is about throughput, latency, and overall speed -- distinct from Fault (is it up?) and Configuration (is it set right?).",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "question": "Which command would you run to quickly check the status of every interface on a router?",
                "options": ["show version", "show running-config", "show ip interface brief", "show cdp neighbors"],
                "answer": 2,
                "explanation": "show ip interface brief gives a one-line-per-interface status summary -- the command you'll run constantly.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "question": "SNMPv2c sends its community string in plain text.",
                "answer": True,
                "explanation": "SNMPv2c has no encryption -- the community string (acting as a password) travels unencrypted, which is why SNMPv3 is preferred for production.",
            },
            {
                "id": "q4",
                "type": "multiple_choice",
                "question": "What does NetFlow actually record?",
                "options": [
                    "Full packet contents",
                    "Traffic metadata like source, destination, ports, and byte counts",
                    "Only the router's CPU usage",
                    "Wi-Fi signal strength",
                ],
                "answer": 1,
                "explanation": "NetFlow captures who-talked-to-who metadata, not payload content -- useful for traffic analysis without inspecting actual data.",
            },
            {
                "id": "q5",
                "type": "multiple_choice",
                "question": "What's the main benefit of IP SLA?",
                "options": [
                    "It encrypts management traffic",
                    "It proactively detects issues like latency spikes before users report them",
                    "It blocks unauthorized traffic",
                    "It assigns IP addresses automatically",
                ],
                "answer": 1,
                "explanation": "IP SLA runs scheduled synthetic tests (like automated pings) so problems surface in monitoring before a user ever calls the help desk.",
            },
            {
                "id": "q6",
                "type": "multiple_choice",
                "question": "Why is `copy running-config startup-config` an important habit?",
                "options": [
                    "It encrypts the configuration",
                    "It saves your active config so changes survive a reboot",
                    "It pings a remote server",
                    "It disables unused ports",
                ],
                "answer": 1,
                "explanation": "running-config is only in memory. Without saving it to startup-config, a reboot wipes out everything you just configured.",
            },
        ],
    },
}
