# ─────────────────────────────────────────────────────────────────────────────
# O-O/S-S — Object-Oriented Security Scripting chapter
# Drop this dict into the CHAPTERS list in app/content.py
# Matches your existing chapter/lesson structure exactly.
# ─────────────────────────────────────────────────────────────────────────────
from .ch6_l3b import CH6_L3B


OOSS_CHAPTER = {
    "id": "ch6",
    "number": 6,
    "title": "Security Scripting (O-O/S-S)",
    "subtitle": "OOP · Recursion · Network Automation · Forensics",
    "description": (
        "Apply Python to real cybersecurity tasks. "
        "Build OOP scanners, recursive directory crawlers, "
        "log analyzers, and a working port scanner — "
        "covering every week of object-oriented security-scripting. "
        "Includes Capstone — Porting arc-sec-audit to Python."
    ),
    "lessons": [

        # ── Week 1 ────────────────────────────────────────────────────────────
        {
            "id": "ch6_l1",
            "title": "Types & OOP — The Security Script Foundation",
            "duration": "20 min",
            "objectives": [
                "Understand why Python types matter in security contexts",
                "Create a class with __init__, attributes, and methods",
                "Model a real security concept (Host) as an object",
            ],
            "sections": [
                {
                    "heading": "Why Types Matter in Security Scripts",
                    "body": (
                        "The wrong type breaks your tool silently. "
                        "An IP address stored as an int behaves completely "
                        "differently than one stored as a str. "
                        "Use type() constantly when debugging security scripts."
                    ),
                    "code": (
                        'ip = "192.168.1.1"   # str — always quote IPs\n'
                        "port = 443            # int — numeric\n"
                        "is_open = True        # bool — port state\n"
                        'flags = {"syn": True, "ack": False}  # dict\n'
                        "\n"
                        "print(type(ip))       # <class 'str'>\n"
                        "print(type(port))     # <class 'int'>"
                    ),
                    "note": None,
                },
                {
                    "heading": "Your First Security Class — Host",
                    "body": (
                        "OOP means modelling real things as objects. "
                        "A Host class holds an IP, its open ports, "
                        "and methods to interact with it. "
                        "__init__ runs the moment you create an instance. "
                        "self refers to that specific object."
                    ),
                    "code": (
                        "class Host:\n"
                        "    def __init__(self, ip):\n"
                        "        self.ip = ip\n"
                        "        self.open_ports = []\n"
                        "\n"
                        "    def add_port(self, port):\n"
                        "        self.open_ports.append(port)\n"
                        "\n"
                        "    def report(self):\n"
                        '        print(f"Host: {self.ip}")\n'
                        '        print(f"Open ports: {self.open_ports}")\n'
                        "\n"
                        'h = Host("192.168.1.10")\n'
                        "h.add_port(22)\n"
                        "h.add_port(80)\n"
                        "h.report()"
                    ),
                    "note": None,
                },
                {
                    "heading": "Dicts as Lookup Tables",
                    "body": (
                        "In security scripts, dicts are your constant companion — "
                        "port-to-service mapping, IP-to-hostname, "
                        "flag-to-value. Memorise dict syntax cold."
                    ),
                    "code": (
                        "services = {\n"
                        '    22:   "SSH",\n'
                        '    80:   "HTTP",\n'
                        '    443:  "HTTPS",\n'
                        '    3389: "RDP",\n'
                        "}\n"
                        "\n"
                        'print(services.get(443, "Unknown"))  # HTTPS\n'
                        'print(services.get(9999, "Unknown")) # Unknown'
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a Network Asset",
                "instruction": (
                    "Create a NetworkAsset class with ip, hostname, and "
                    "a list of services. Add two services and print a summary."
                ),
                "starter_code": (
                    "class NetworkAsset:\n"
                    "    def __init__(self, ip, hostname):\n"
                    "        self.ip = ip\n"
                    "        self.hostname = hostname\n"
                    "        self.services = []\n"
                    "\n"
                    "    def add_service(self, name, port):\n"
                    '        self.services.append({"name": name, "port": port})\n'
                    "\n"
                    "    def summary(self):\n"
                    '        print(f"{self.hostname} ({self.ip})")\n'
                    "        for s in self.services:\n"
                    "            print(f\"  {s['port']:>5}  {s['name']}\")\n"
                    "\n"
                    'asset = NetworkAsset("10.0.0.1", "router.local")\n'
                    'asset.add_service("SSH", 22)\n'
                    'asset.add_service("HTTPS", 443)\n'
                    "asset.summary()"
                ),
            },
        },

        # ── Week 2 ────────────────────────────────────────────────────────────
        {
            "id": "ch6_l2",
            "title": "Recursion — Scanning Nested Directories",
            "duration": "20 min",
            "objectives": [
                "Explain what recursion is and why it needs a base case",
                "Write a recursive directory scanner",
                "Compare recursion vs iteration — know the trade-offs",
            ],
            "sections": [
                {
                    "heading": "What Recursion Is",
                    "body": (
                        "A recursive function calls itself to solve a smaller "
                        "version of the same problem. "
                        "Every recursive function needs two things: "
                        "(1) a base case — when to stop, and "
                        "(2) a recursive case — calling itself with a smaller input. "
                        "Forget the base case and Python raises RecursionError."
                    ),
                    "code": (
                        "def countdown(n):\n"
                        "    if n == 0:           # base case\n"
                        '        print("Done!")\n'
                        "        return\n"
                        "    print(n)\n"
                        "    countdown(n - 1)     # recursive case\n"
                        "\n"
                        "countdown(5)"
                    ),
                    "note": None,
                },
                {
                    "heading": "Recursive Directory Scanner — Real Security Use",
                    "body": (
                        "Malware hides in deeply nested directories. "
                        "A recursive scanner handles any depth automatically — "
                        "you don't need to know how deep the tree goes. "
                        "This pattern is used in forensic tools and AV scanners."
                    ),
                    "code": (
                        "import os\n"
                        "\n"
                        "def scan_directory(path, depth=0):\n"
                        '    indent = "  " * depth\n'
                        "    try:\n"
                        "        for entry in os.scandir(path):\n"
                        "            print(f\"{indent}{entry.name}\")\n"
                        "            if entry.is_dir():\n"
                        "                scan_directory(entry.path, depth + 1)\n"
                        "    except PermissionError:\n"
                        "        print(f\"{indent}[permission denied]\")\n"
                        "\n"
                        'scan_directory(".")'
                    ),
                    "note": "Run this locally — it scans your actual filesystem from the current directory.",
                },
                {
                    "heading": "Recursion vs Iteration — The Real Trade-off",
                    "body": (
                        "Advantage: clean code for tree-like structures, handles unlimited depth. "
                        "Disadvantage: each call uses stack memory. "
                        "Python's default limit is 1000 calls. "
                        "Very deep trees crash with RecursionError. "
                        "For unknown-depth trees in production, use an iterative stack instead."
                    ),
                    "code": (
                        "import sys\n"
                        "print(sys.getrecursionlimit())  # 1000\n"
                        "\n"
                        "# Iterative alternative — safer for very deep trees\n"
                        "import os\n"
                        "\n"
                        "def scan_iterative(start_path):\n"
                        "    stack = [start_path]\n"
                        "    while stack:\n"
                        "        current = stack.pop()\n"
                        "        print(current)\n"
                        "        try:\n"
                        "            for entry in os.scandir(current):\n"
                        "                if entry.is_dir():\n"
                        "                    stack.append(entry.path)\n"
                        "        except PermissionError:\n"
                        "            pass\n"
                        "\n"
                        'scan_iterative(".")'
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Recursive File Counter",
                "instruction": (
                    "Write a recursive function count_files(path) that returns "
                    "the total number of files (not directories) inside a directory "
                    "and all its subdirectories."
                ),
                "starter_code": (
                    "import os\n"
                    "\n"
                    "def count_files(path):\n"
                    "    total = 0\n"
                    "    try:\n"
                    "        for entry in os.scandir(path):\n"
                    "            if entry.is_file():\n"
                    "                total += 1\n"
                    "            elif entry.is_dir():\n"
                    "                total += count_files(entry.path)  # recurse\n"
                    "    except PermissionError:\n"
                    "        pass\n"
                    "    return total\n"
                    "\n"
                    'result = count_files(".")\n'
                    'print(f"Total files found: {result}")'
                ),
            },
        },

        # ── Week 3 ────────────────────────────────────────────────────────────
        {
            "id": "ch6_l3",
            "title": "Searching & Sorting Security Data",
            "duration": "15 min",
            "objectives": [
                "Compare linear vs binary search — know when to use each",
                "Sort log entries by severity using sorted() and a key function",
                "Apply these patterns to real security data",
            ],
            "sections": [
                {
                    "heading": "Linear vs Binary Search",
                    "body": (
                        "Linear search checks every item — O(n), works on anything. "
                        "Binary search halves the list each time — O(log n), "
                        "but requires a sorted list. "
                        "Searching a blocklist of 1 million IPs: "
                        "linear = up to 1,000,000 checks, "
                        "binary = at most 20 checks."
                    ),
                    "code": (
                        "# Linear — O(n)\n"
                        "def linear_search(ip_list, target):\n"
                        "    for ip in ip_list:\n"
                        "        if ip == target:\n"
                        "            return True\n"
                        "    return False\n"
                        "\n"
                        "# Binary — O(log n), list must be sorted\n"
                        "def binary_search(ip_list, target):\n"
                        "    low, high = 0, len(ip_list) - 1\n"
                        "    while low <= high:\n"
                        "        mid = (low + high) // 2\n"
                        "        if ip_list[mid] == target:\n"
                        "            return True\n"
                        "        elif ip_list[mid] < target:\n"
                        "            low = mid + 1\n"
                        "        else:\n"
                        "            high = mid - 1\n"
                        "    return False\n"
                        "\n"
                        'blocklist = ["10.0.0.1", "10.0.0.5", "192.168.1.99"]\n'
                        'print(binary_search(sorted(blocklist), "10.0.0.5"))'
                    ),
                    "note": None,
                },
                {
                    "heading": "Sorting Logs by Severity",
                    "body": (
                        "Raw logs are chronological. "
                        "For forensics you want them sorted by severity, IP, or event type. "
                        "Python's sorted() with a key= function does this in one line."
                    ),
                    "code": (
                        "logs = [\n"
                        '    {"ip": "10.0.0.3", "severity": 3, "event": "port scan"},\n'
                        '    {"ip": "10.0.0.1", "severity": 9, "event": "brute force"},\n'
                        '    {"ip": "10.0.0.2", "severity": 1, "event": "ping"},\n'
                        "]\n"
                        "\n"
                        "by_severity = sorted(logs, key=lambda x: x[\"severity\"], reverse=True)\n"
                        "\n"
                        "for log in by_severity:\n"
                        "    print(f\"[{log['severity']}] {log['ip']} — {log['event']}\")"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Blocklist Lookup",
                "instruction": (
                    "Given a sorted list of blocked IPs, use binary_search "
                    "to check if '10.0.0.7' and '172.16.0.1' are blocked. "
                    "Print BLOCKED or ALLOWED for each."
                ),
                "starter_code": (
                    "def binary_search(ip_list, target):\n"
                    "    low, high = 0, len(ip_list) - 1\n"
                    "    while low <= high:\n"
                    "        mid = (low + high) // 2\n"
                    "        if ip_list[mid] == target:\n"
                    "            return True\n"
                    "        elif ip_list[mid] < target:\n"
                    "            low = mid + 1\n"
                    "        else:\n"
                    "            high = mid - 1\n"
                    "    return False\n"
                    "\n"
                    "blocklist = sorted([\n"
                    '    "10.0.0.1", "10.0.0.7", "10.0.0.99",\n'
                    '    "192.168.1.5", "192.168.1.50"\n'
                    "])\n"
                    "\n"
                    'targets = ["10.0.0.7", "172.16.0.1"]\n'
                    "for ip in targets:\n"
                    "    status = \"BLOCKED\" if binary_search(blocklist, ip) else \"ALLOWED\"\n"
                    '    print(f"{ip}: {status}")'
                ),
            },
        },

        CH6_L3B,  # ← sorting algorithms

        # ── Week 4 ────────────────────────────────────────────────────────────
        {
            "id": "ch6_l4",
            "title": "Network Automation — OOP Port Scanner",
            "duration": "25 min",
            "objectives": [
                "Understand how sockets work at the TCP level",
                "Use socket.connect_ex() to probe open ports",
                "Wrap the scanner in an OOP class with a clean report() method",
            ],
            "sections": [
                {
                    "heading": "Sockets — The Foundation",
                    "body": (
                        "Before Scapy, Nmap, or anything fancy — understand sockets. "
                        "A socket is a connection endpoint. "
                        "connect_ex() returns 0 if the port is open, non-zero if closed/filtered. "
                        "This is how every port scanner works under the hood."
                    ),
                    "code": (
                        "import socket\n"
                        "\n"
                        "def check_port(host, port, timeout=1):\n"
                        '    """Returns True if port is open."""\n'
                        "    try:\n"
                        "        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
                        "        s.settimeout(timeout)\n"
                        "        result = s.connect_ex((host, port))\n"
                        "        s.close()\n"
                        "        return result == 0\n"
                        "    except socket.error:\n"
                        "        return False\n"
                        "\n"
                        '# scanme.nmap.org is a legal test target\n'
                        'target = "scanme.nmap.org"\n'
                        "for port in [22, 80, 443]:\n"
                        "    status = \"OPEN\" if check_port(target, port) else \"closed\"\n"
                        '    print(f"Port {port}: {status}")'
                    ),
                    "note": "scanme.nmap.org is provided by the Nmap project specifically for legal scanning practice.",
                },
                {
                    "heading": "OOP Port Scanner — Week 4 Pattern",
                    "body": (
                        "This is the Week 4 pattern: "
                        "data in __init__, "
                        "logic in scan(), "
                        "output in report(). "
                        "One class, clean interface, reusable anywhere."
                    ),
                    "code": (
                        "import socket\n"
                        "from datetime import datetime\n"
                        "\n"
                        "class PortScanner:\n"
                        "    def __init__(self, target, ports):\n"
                        "        self.target = target\n"
                        "        self.ports = ports\n"
                        "        self.results = {}\n"
                        "\n"
                        "    def scan(self):\n"
                        "        print(f\"Scanning {self.target} — {datetime.now()}\")\n"
                        "        for port in self.ports:\n"
                        "            try:\n"
                        "                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
                        "                s.settimeout(0.5)\n"
                        "                self.results[port] = s.connect_ex((self.target, port)) == 0\n"
                        "                s.close()\n"
                        "            except socket.error:\n"
                        "                self.results[port] = False\n"
                        "\n"
                        "    def report(self):\n"
                        "        for port, is_open in self.results.items():\n"
                        "            status = \"OPEN  ✓\" if is_open else \"closed\"\n"
                        "            print(f\"  {port:>5}  {status}\")\n"
                        "\n"
                        'scanner = PortScanner("scanme.nmap.org", [22, 80, 443])\n'
                        "scanner.scan()\n"
                        "scanner.report()"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Extend the Scanner",
                "instruction": (
                    "Add a method open_ports() to PortScanner that returns "
                    "a list of only the open port numbers. "
                    "Then print a summary: 'X of Y ports open'."
                ),
                "starter_code": (
                    "import socket\n"
                    "\n"
                    "class PortScanner:\n"
                    "    def __init__(self, target, ports):\n"
                    "        self.target = target\n"
                    "        self.ports = ports\n"
                    "        self.results = {}\n"
                    "\n"
                    "    def scan(self):\n"
                    "        for port in self.ports:\n"
                    "            try:\n"
                    "                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
                    "                s.settimeout(0.5)\n"
                    "                self.results[port] = s.connect_ex((self.target, port)) == 0\n"
                    "                s.close()\n"
                    "            except socket.error:\n"
                    "                self.results[port] = False\n"
                    "\n"
                    "    def open_ports(self):\n"
                    "        return [p for p, open_ in self.results.items() if open_]\n"
                    "\n"
                    "    def report(self):\n"
                    "        opens = self.open_ports()\n"
                    "        print(f\"{len(opens)} of {len(self.ports)} ports open\")\n"
                    "        for p in opens:\n"
                    "            print(f\"  {p:>5}  OPEN\")\n"
                    "\n"
                    'scanner = PortScanner("scanme.nmap.org", [22, 80, 443, 8080])\n'
                    "scanner.scan()\n"
                    "scanner.report()"
                ),
            },
        },

        # ── Week 5 ────────────────────────────────────────────────────────────
        {
            "id": "ch6_l5",
            "title": "Forensics & Inheritance — Putting It Together",
            "duration": "20 min",
            "objectives": [
                "Parse log files with regex to find suspicious IPs",
                "Use Counter to rank threats by frequency",
                "Build a scanner hierarchy with inheritance",
            ],
            "sections": [
                {
                    "heading": "Log Analysis — Finding Brute Force Attacks",
                    "body": (
                        "Most forensic work is log analysis — reading, filtering, flagging. "
                        "Python's re module and collections.Counter turn raw auth logs "
                        "into a ranked threat list in under 10 lines."
                    ),
                    "code": (
                        "import re\n"
                        "from collections import Counter\n"
                        "\n"
                        "# Simulated auth.log snippet\n"
                        "log_data = \"\"\"\n"
                        "Failed password for root from 10.0.0.5 port 22\n"
                        "Failed password for root from 10.0.0.5 port 22\n"
                        "Failed password for admin from 192.168.1.99 port 22\n"
                        "Failed password for root from 10.0.0.5 port 22\n"
                        "Accepted password for user from 10.0.0.10 port 22\n"
                        "\"\"\"\n"
                        "\n"
                        "pattern = re.compile(r\"Failed password.*from (\\d+\\.\\d+\\.\\d+\\.\\d+)\")\n"
                        "failed_ips = pattern.findall(log_data)\n"
                        "counts = Counter(failed_ips)\n"
                        "\n"
                        "print(\"Top brute-force sources:\")\n"
                        "for ip, n in counts.most_common():\n"
                        "    print(f\"  {ip:>15}  {n} attempts\")"
                    ),
                    "note": None,
                },
                {
                    "heading": "Inheritance — Building a Scanner Suite",
                    "body": (
                        "Inheritance means a child class gets everything from the parent. "
                        "Build a base Scanner once, then extend it for port scanning, "
                        "web scanning, vuln scanning — all sharing the same core log() and report(). "
                        "class Child(Parent): — that's all inheritance is."
                    ),
                    "code": (
                        "class Scanner:\n"
                        '    """Base class shared by all scanner types."""\n'
                        "    def __init__(self, target):\n"
                        "        self.target = target\n"
                        "        self.findings = []\n"
                        "\n"
                        "    def log(self, message):\n"
                        "        self.findings.append(message)\n"
                        "        print(f\"[{self.target}] {message}\")\n"
                        "\n"
                        "    def report(self):\n"
                        "        print(f\"\\n=== {self.target} ===\")\n"
                        "        for f in self.findings:\n"
                        "            print(f\"  • {f}\")\n"
                        "\n"
                        "\n"
                        "class WebScanner(Scanner):\n"
                        '    """Inherits Scanner, adds HTTP header checks."""\n'
                        "    def check_headers(self, headers):\n"
                        "        if \"X-Frame-Options\" not in headers:\n"
                        "            self.log(\"Missing X-Frame-Options\")\n"
                        "        if \"Strict-Transport-Security\" not in headers:\n"
                        "            self.log(\"Missing HSTS header\")\n"
                        "\n"
                        "\n"
                        'ws = WebScanner("example.com")\n'
                        'ws.check_headers({"Content-Type": "text/html"})\n'
                        "ws.report()"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a VulnScanner",
                "instruction": (
                    "Extend the Scanner base class to create a VulnScanner. "
                    "Add a method check_ports(open_ports) that logs a warning "
                    "if port 23 (Telnet) or 21 (FTP) is in the list — "
                    "both are insecure protocols."
                ),
                "starter_code": (
                    "class Scanner:\n"
                    "    def __init__(self, target):\n"
                    "        self.target = target\n"
                    "        self.findings = []\n"
                    "\n"
                    "    def log(self, message):\n"
                    "        self.findings.append(message)\n"
                    "        print(f\"[{self.target}] {message}\")\n"
                    "\n"
                    "    def report(self):\n"
                    "        print(f\"\\n=== {self.target} ===\")\n"
                    "        for f in self.findings:\n"
                    "            print(f\"  • {f}\")\n"
                    "\n"
                    "\n"
                    "class VulnScanner(Scanner):\n"
                    "    INSECURE_PORTS = {\n"
                    '        21: "FTP — cleartext file transfer",\n'
                    '        23: "Telnet — cleartext remote access",\n'
                    '        80: "HTTP — unencrypted web",\n'
                    "    }\n"
                    "\n"
                    "    def check_ports(self, open_ports):\n"
                    "        for port in open_ports:\n"
                    "            if port in self.INSECURE_PORTS:\n"
                    "                self.log(f\"Port {port} open: {self.INSECURE_PORTS[port]}\")\n"
                    "\n"
                    "\n"
                    'vs = VulnScanner("target.local")\n'
                    "vs.check_ports([22, 23, 80, 443])\n"
                    "vs.report()"
                ),
            },
        },
        # ── Capstone ──────────────────────────────────────────────────────────
        {
            "id": "ch6_l6",
            "title": "Capstone — Porting arc-sec-audit to Python",
            "duration": "30 min",
            "objectives": [
                "Understand how a real bash security tool maps to Python structure",
                "Build an OOP Auditor base class with counters and output helpers",
                "Translate sysctl, stat, grep, and find patterns to Python equivalents",
                "Write runnable exercises on the pure-Python parts of the tool",
            ],
            "sections": [
                {
                    "heading": "What arc-sec-audit Does",
                    "body": (
                        "arc-sec-audit is a 392-line bash workstation hardening scanner. "
                        "It runs nine check categories — SSH config, kernel params, "
                        "file permissions, SUID binaries, world-writable files, "
                        "sudoers, listening services, packages, and system integrity — "
                        "then prints a colour-coded pass / warn / fail summary. "
                        "Porting it to Python means: one class per concept, "
                        "subprocess replaces shell commands, pathlib replaces stat, "
                        "re replaces grep."
                    ),
                    "code": (
                        "# bash → python pattern map\n"
                        "#\n"
                        "# _pass=0                    self.passed = 0\n"
                        "# _ok()  { (( _pass++ )) }  def ok(self, msg): ...\n"
                        "# _check_ssh()              def check(a): in checks/ssh.py\n"
                        "# sysctl -n key             subprocess.run(['sysctl','-n',key])\n"
                        "# stat -c '%a' file         oct(Path(file).stat().st_mode)[-3:]\n"
                        "# grep -rihE pat | tail -1  re.finditer() — take last match\n"
                        "# find / -perm -4000        subprocess.run(['find',...])\n"
                    ),
                    "note": None,
                },
                {
                    "heading": "The Auditor Base Class",
                    "body": (
                        "Every bash script has global counters and output helpers. "
                        "In Python those become an Auditor class. "
                        "One instance is created at startup and passed into every check function. "
                        "This is the OOP pattern from lesson 1 applied to a real tool."
                    ),
                    "code": (
                        "class Auditor:\n"
                        "    def __init__(self):\n"
                        "        self.passed   = 0\n"
                        "        self.warnings = 0\n"
                        "        self.failed   = 0\n"
                        "\n"
                        "    def ok(self, msg):\n"
                        "        print(f'  ✓  {msg}')\n"
                        "        self.passed += 1\n"
                        "\n"
                        "    def warn(self, msg):\n"
                        "        print(f'  !  {msg}')\n"
                        "        self.warnings += 1\n"
                        "\n"
                        "    def fail(self, msg):\n"
                        "        print(f'  ✗  {msg}')\n"
                        "        self.failed += 1\n"
                        "\n"
                        "    def summary(self):\n"
                        "        print(f'  {self.passed} passed  ·  '\n"
                        "              f'{self.warnings} warnings  ·  '\n"
                        "              f'{self.failed} failed')\n"
                        "\n"
                        "a = Auditor()\n"
                        "a.ok('PermitRootLogin  no')\n"
                        "a.warn('PasswordAuthentication  yes  — should be no')\n"
                        "a.summary()"
                    ),
                    "note": None,
                },
                {
                    "heading": "File Permissions — pathlib Instead of stat",
                    "body": (
                        "The bash script shells out to stat -c \"%a\" to get octal permissions. "
                        "In Python, pathlib.Path.stat() gives you the mode directly. "
                        "oct(mode)[-3:] slices out the three permission digits. "
                        "No subprocess needed — pure Python, runs anywhere."
                    ),
                    "code": (
                        "from pathlib import Path\n"
                        "\n"
                        "def perm_chk(auditor, path, want):\n"
                        "    p = Path(path)\n"
                        "    if not p.exists():\n"
                        "        auditor.info(f'{path}  not found — skipping')\n"
                        "        return\n"
                        "    actual = oct(p.stat().st_mode)[-3:]\n"
                        "    if actual == want:\n"
                        "        auditor.ok(f'{path}  {actual}')\n"
                        "    else:\n"
                        "        auditor.warn(f'{path}  {actual} — want {want}')\n"
                        "\n"
                        "# bash: actual=$(stat -c '%a' /etc/shadow)"
                    ),
                    "note": "This check runs fine in the browser — no subprocess, pure pathlib.",
                },
                {
                    "heading": "SSH Config — re Instead of grep",
                    "body": (
                        "The bash version greps sshd_config for directives and pipes through awk. "
                        "Python reads the file as a string and uses re.finditer(). "
                        "sshd processes config top-to-bottom and last entry wins, "
                        "so we take the last regex match, not the first."
                    ),
                    "code": (
                        "import re\n"
                        "\n"
                        "fake_cfg = '''\n"
                        "PermitRootLogin yes\n"
                        "PasswordAuthentication yes\n"
                        "PermitRootLogin no\n"
                        "'''\n"
                        "\n"
                        "pattern = re.compile(\n"
                        "    r'^PermitRootLogin\\s+(\\S+)',\n"
                        "    re.IGNORECASE | re.MULTILINE\n"
                        ")\n"
                        "matches = list(pattern.finditer(fake_cfg))\n"
                        "last = matches[-1].group(1).lower() if matches else None\n"
                        "print(last)  # no — last entry wins"
                    ),
                    "note": None,
                },
                {
                    "heading": "subprocess — The Bridge to OS Commands",
                    "body": (
                        "Checks that need sysctl, ss, find, or sudo shell out via subprocess.run(). "
                        "The Auditor wraps this in a run() helper that always returns a string — "
                        "empty string on failure — so every check handles missing tools gracefully. "
                        "subprocess calls need a real Linux environment. "
                        "Use them locally: sudo python arc_sec_audit.py"
                    ),
                    "code": (
                        "import subprocess\n"
                        "\n"
                        "# inside Auditor class:\n"
                        "def run(self, cmd, sudo=False, timeout=10):\n"
                        "    if sudo:\n"
                        "        cmd = ['sudo'] + cmd\n"
                        "    try:\n"
                        "        result = subprocess.run(\n"
                        "            cmd, capture_output=True,\n"
                        "            text=True, timeout=timeout\n"
                        "        )\n"
                        "        return result.stdout.strip()\n"
                        "    except (subprocess.TimeoutExpired,\n"
                        "            FileNotFoundError, PermissionError):\n"
                        "        return ''\n"
                        "\n"
                        "def sysctl_chk(self, key, want, label, mode='exact'):\n"
                        "    val_str = self.run(['sysctl', '-n', key])\n"
                        "    if not val_str:\n"
                        "        self.info(f'{label}  (not available)')\n"
                        "        return\n"
                        "    val = int(val_str)\n"
                        "    if mode == 'min' and val >= want:\n"
                        "        self.ok(f'{label}  {val}')\n"
                        "    elif mode == 'exact' and val == want:\n"
                        "        self.ok(f'{label}  {val}')\n"
                        "    else:\n"
                        "        self.warn(f'{label}  got {val}, want {want}')"
                    ),
                    "note": "Run locally: sudo python arc_sec_audit.py — subprocess requires a real Linux shell.",
                },
            ],
            "exercise": {
                "title": "Build a Mini Auditor",
                "instruction": (
                    "Build a miniature arc-sec-audit. "
                    "Write check_shadow_perm() — takes an auditor and a simulated "
                    "permission string, calls ok() if it matches '640', warn() otherwise. "
                    "Then write check_root_login() — takes a config string, "
                    "uses re to find the last PermitRootLogin value, "
                    "calls ok() if 'no', warn() otherwise. "
                    "Run both and print the summary."
                ),
                "starter_code": (
                    "import re\n"
                    "\n"
                    "class Auditor:\n"
                    "    def __init__(self):\n"
                    "        self.passed   = 0\n"
                    "        self.warnings = 0\n"
                    "        self.failed   = 0\n"
                    "\n"
                    "    def ok(self, msg):\n"
                    "        print(f'  ✓  {msg}')\n"
                    "        self.passed += 1\n"
                    "\n"
                    "    def warn(self, msg):\n"
                    "        print(f'  !  {msg}')\n"
                    "        self.warnings += 1\n"
                    "\n"
                    "    def summary(self):\n"
                    "        print(f'\\n  {self.passed} passed  ·  {self.warnings} warnings')\n"
                    "\n"
                    "\n"
                    "def check_shadow_perm(a, simulated_perm):\n"
                    "    want = '640'\n"
                    "    if simulated_perm == want:\n"
                    "        a.ok(f'/etc/shadow  {simulated_perm}')\n"
                    "    else:\n"
                    "        a.warn(f'/etc/shadow  {simulated_perm} — want {want}')\n"
                    "\n"
                    "\n"
                    "def check_root_login(a, cfg_text):\n"
                    "    pattern = re.compile(\n"
                    "        r'^PermitRootLogin\\s+(\\S+)',\n"
                    "        re.IGNORECASE | re.MULTILINE\n"
                    "    )\n"
                    "    matches = list(pattern.finditer(cfg_text))\n"
                    "    val = matches[-1].group(1).lower() if matches else None\n"
                    "    if val == 'no':\n"
                    "        a.ok(f'PermitRootLogin  {val}')\n"
                    "    else:\n"
                    "        a.warn(f'PermitRootLogin  {val or chr(117)+chr(110)+chr(115)+chr(101)+chr(116)}  — should be no')\n"
                    "\n"
                    "\n"
                    "a = Auditor()\n"
                    "check_shadow_perm(a, '640')\n"
                    "check_shadow_perm(a, '644')\n"
                    "cfg = '''\n"
                    "PermitRootLogin yes\n"
                    "PermitRootLogin no\n"
                    "'''\n"
                    "check_root_login(a, cfg)\n"
                    "a.summary()"
                ),
            },
        },
    ],
}
