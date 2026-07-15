PYTHON_ALGORITHMS_CHAPTER = {
    "id": "ch-python-algorithms",
    "number": 12,
    "title": "Python Algorithms & Security Scripting",
    "subtitle": "Searching · Sorting · Bash-to-Python · OOP Auditor",
    "description": (
        "Searching and sorting are the bread and butter of any script that works "
        "with lists of IPs, ports, CVEs, or alert severities. Then take it further: "
        "learn the patterns that turn a 392-line bash security audit into clean, "
        "testable Python — subprocess, pathlib, and an OOP Auditor class that "
        "structures every check the same way."
    ),
    "further_reading": [
        {"title": "Python Algorithms — Pocket Reference", "url": "/static/pdfs/python-algorithms-pocket-reference.pdf"},
    ],
    "lessons": [

        # ── Lesson 1 ─────────────────────────────────────────────────────────
        {
            "id": "pa-l1-searching",
            "title": "Searching Algorithms",
            "duration": "20 min",
            "objectives": [
                "Choose between linear and binary search based on whether the data is sorted",
                "Implement LinearSearcher and BinarySearcher as reusable OOP classes",
                "Apply both to real security examples: port lists, IP blacklists",
            ],
            "sections": [
                {
                    "heading": "The Big Picture",
                    "body": (
                        "Searching means finding whether something is in a collection "
                        "and where. In security scripting this comes up constantly: "
                        "is port 4444 in the list of open ports on this host? "
                        "Is this IP in the known-bad blacklist? Is this CVE ID in "
                        "the patched list?\n\n"
                        "Two algorithms cover 95% of cases: Linear (works on anything, "
                        "O(n)) and Binary (lightning fast on sorted data, O(log n))."
                    ),
                    "code": None,
                    "note": None,
                },
                {
                    "heading": "Linear Search — Check Every Item",
                    "body": (
                        "Walk through the list from the beginning, compare each item to "
                        "the target, return the position if found. Simple. Works on any "
                        "list, sorted or not. The downside: worst case you look at every "
                        "element — O(n). Fine for small or unsorted lists; slow for "
                        "large sorted ones."
                    ),
                    "code": (
                        "class linear_searcher:\n"
                        "    def __init__(self, items):\n"
                        "        self.items = items\n"
                        "\n"
                        "    def find(self, target):\n"
                        "        for index, item in enumerate(self.items):\n"
                        "            if item == target:\n"
                        "                return index\n"
                        "        return -1\n"
                        "\n"
                        "    def contains(self, target):\n"
                        "        return self.find(target) != -1\n"
                        "\n"
                        "\n"
                        "# Security example: is a suspicious port in the open-port scan list?\n"
                        "open_ports = [80, 443, 22, 8080, 3389, 4444, 5900]\n"
                        "SUSPICIOUS = {4444, 1337, 31337, 5900}\n"
                        "\n"
                        "scanner = linear_searcher(open_ports)\n"
                        "\n"
                        "print('Open port audit:')\n"
                        "for port in open_ports:\n"
                        "    flag = ' <- SUSPICIOUS' if port in SUSPICIOUS else ''\n"
                        "    idx = scanner.find(port)\n"
                        "    print(f'  index {idx}: port {port}{flag}')\n"
                        "\n"
                        "print(f'\\nPort 4444 found: {scanner.contains(4444)}')\n"
                        "print(f'Port 53  found: {scanner.contains(53)}')"
                    ),
                    "note": None,
                },
                {
                    "heading": "Binary Search — Halve the Space",
                    "body": (
                        "Binary search requires a sorted list. It works by looking at "
                        "the middle element: if the target is smaller, search the left "
                        "half; if larger, search the right half. Each comparison cuts "
                        "the remaining search space in half — O(log n). A million-item "
                        "sorted blacklist takes at most 20 comparisons."
                    ),
                    "code": (
                        "class binary_searcher:\n"
                        "    def __init__(self, items):\n"
                        "        self.items = sorted(items)\n"
                        "\n"
                        "    def find(self, target):\n"
                        "        low, high = 0, len(self.items) - 1\n"
                        "        while low <= high:\n"
                        "            mid = (low + high) // 2\n"
                        "            if self.items[mid] == target:\n"
                        "                return mid\n"
                        "            elif target < self.items[mid]:\n"
                        "                high = mid - 1\n"
                        "            else:\n"
                        "                low = mid + 1\n"
                        "        return -1\n"
                        "\n"
                        "    def contains(self, target):\n"
                        "        return self.find(target) != -1\n"
                        "\n"
                        "\n"
                        "# Security example: is this IP in the known-bad blacklist?\n"
                        "blacklist = [\n"
                        "    '10.0.0.5', '10.0.0.12', '10.0.0.20', '10.0.0.33',\n"
                        "    '10.0.0.50', '10.0.0.99', '192.168.50.1',\n"
                        "]\n"
                        "\n"
                        "checker = binary_searcher(blacklist)\n"
                        "\n"
                        "test_ips = ['10.0.0.20', '10.0.0.21', '192.168.50.1', '8.8.8.8']\n"
                        "print('IP blacklist check:')\n"
                        "for ip in test_ips:\n"
                        "    found = checker.contains(ip)\n"
                        "    status = 'BLOCKED' if found else 'ALLOWED'\n"
                        "    print(f'  {ip:18} -> {status}')\n"
                        "\n"
                        "print(f'\\nList is pre-sorted internally: {checker.items[:4]} ...')"
                    ),
                    "note": (
                        "Binary search silently sorts the input at construction time. "
                        "The reported index refers to the sorted order, not the original."
                    ),
                },
            ],
            "exercise": {
                "title": "CVE Lookup — Linear vs Binary",
                "instruction": (
                    "You have a list of CVE IDs (already sorted). Implement both a "
                    "linear_searcher and binary_searcher version of a function that "
                    "checks whether a given CVE is in the patched list. Then count how "
                    "many comparisons each approach would theoretically need to find "
                    "the last item in the list (linear = n, binary = log2(n) rounded up)."
                ),
                "starter_code": (
                    "import math\n"
                    "\n"
                    "class linear_searcher:\n"
                    "    def __init__(self, items):\n"
                    "        self.items = items\n"
                    "\n"
                    "    def find(self, target):\n"
                    "        for index, item in enumerate(self.items):\n"
                    "            if item == target:\n"
                    "                return index\n"
                    "        return -1\n"
                    "\n"
                    "\n"
                    "class binary_searcher:\n"
                    "    def __init__(self, items):\n"
                    "        self.items = sorted(items)\n"
                    "\n"
                    "    def find(self, target):\n"
                    "        low, high = 0, len(self.items) - 1\n"
                    "        while low <= high:\n"
                    "            mid = (low + high) // 2\n"
                    "            if self.items[mid] == target:\n"
                    "                return mid\n"
                    "            elif target < self.items[mid]:\n"
                    "                high = mid - 1\n"
                    "            else:\n"
                    "                low = mid + 1\n"
                    "        return -1\n"
                    "\n"
                    "\n"
                    "patched_cves = [\n"
                    "    'CVE-2023-0001', 'CVE-2023-0045', 'CVE-2023-1234',\n"
                    "    'CVE-2024-0012', 'CVE-2024-1100', 'CVE-2024-5501',\n"
                    "    'CVE-2025-0099', 'CVE-2025-3344', 'CVE-2025-9001',\n"
                    "]\n"
                    "\n"
                    "target = 'CVE-2025-9001'\n"
                    "\n"
                    "linear = linear_searcher(patched_cves)\n"
                    "binary = binary_searcher(patched_cves)\n"
                    "\n"
                    "print(f'Linear search found at index: {linear.find(target)}')\n"
                    "print(f'Binary search found at index: {binary.find(target)}')\n"
                    "\n"
                    "n = len(patched_cves)\n"
                    "print(f'\\nWorst-case comparisons for {n} items:')\n"
                    "print(f'  Linear: {n}')\n"
                    "print(f'  Binary: {math.ceil(math.log2(n))}')"
                ),
            },
        },

        # ── Lesson 2 ─────────────────────────────────────────────────────────
        {
            "id": "pa-l2-sorting",
            "title": "Sorting Algorithms",
            "duration": "30 min",
            "objectives": [
                "Explain the core idea of Bubble, Insertion, Merge, and Quick Sort in one sentence each",
                "Pick the right algorithm for a given scenario using the complexity table",
                "Use Python's built-in sorted() with a lambda key to rank security alerts",
            ],
            "sections": [
                {
                    "heading": "The Algorithm Landscape",
                    "body": (
                        "Eight sorting algorithms are in common use. You don't need to "
                        "implement all of them in production — Python's sorted() uses "
                        "Timsort (a merge+insertion hybrid) and is faster than anything "
                        "you'll write by hand. But understanding the algorithms tells "
                        "you why Timsort beats Bubble Sort by orders of magnitude, and "
                        "which tradeoffs matter when Timsort isn't available.\n\n"
                        "One-liner for each:\n"
                        "Bubble — repeatedly swap neighbours if out of order.\n"
                        "Selection — find the minimum remaining, place it next.\n"
                        "Insertion — take one item at a time, insert into correct spot.\n"
                        "Merge — split in half, sort each half, merge back together.\n"
                        "Quick — pick a pivot; smaller left, larger right; recurse.\n"
                        "Heap — use a binary heap to pull the largest item repeatedly.\n"
                        "Bucket — scatter into value-range buckets, sort each bucket.\n"
                        "Radix — sort digit by digit, least significant first."
                    ),
                    "code": (
                        "# Algorithm comparison table\n"
                        "algorithms = [\n"
                        "    ('Bubble',    'O(n²)',    'O(n²)',    'O(1)',   'Yes', 'teaching only'),\n"
                        "    ('Insertion', 'O(n)',     'O(n²)',    'O(1)',   'Yes', 'great for nearly-sorted'),\n"
                        "    ('Merge',     'O(n logn)','O(n logn)','O(n)',  'Yes', 'reliable, predictable'),\n"
                        "    ('Quick',     'O(n logn)','O(n²)',    'O(logn)','No', 'fastest in practice'),\n"
                        "    ('Heap',      'O(n logn)','O(n logn)','O(1)',   'No', 'good when memory limited'),\n"
                        "    ('Radix',     'O(nk)',    'O(nk)',    'O(n+k)', 'Yes','great for fixed-width ints'),\n"
                        "    ('Timsort',   'O(n)',     'O(n logn)','O(n)',   'Yes','Python built-in default'),\n"
                        "]\n"
                        "\n"
                        "print(f'{'Algorithm':10} {'Best':10} {'Worst':10} {'Space':8} {'Stable':7} Notes')\n"
                        "print('-' * 70)\n"
                        "for row in algorithms:\n"
                        "    print(f'{row[0]:10} {row[1]:10} {row[2]:10} {row[3]:8} {row[4]:7} {row[5]}')"
                    ),
                    "note": None,
                },
                {
                    "heading": "Merge Sort — Reliable O(n log n)",
                    "body": (
                        "Merge sort is the go-to for guaranteed performance. It always "
                        "runs in O(n log n) — unlike Quick Sort which degrades to O(n²) "
                        "in the worst case. The tradeoff is O(n) extra memory. Good "
                        "for sorting event logs or timestamps where predictability "
                        "matters more than squeezing the last bit of speed."
                    ),
                    "code": (
                        "class merge_sorter:\n"
                        "    def sort(self, items):\n"
                        "        arr = items.copy()\n"
                        "        self._merge_sort(arr, 0, len(arr) - 1)\n"
                        "        return arr\n"
                        "\n"
                        "    def _merge_sort(self, arr, left, right):\n"
                        "        if left < right:\n"
                        "            mid = (left + right) // 2\n"
                        "            self._merge_sort(arr, left, mid)\n"
                        "            self._merge_sort(arr, mid + 1, right)\n"
                        "            self._merge(arr, left, mid, right)\n"
                        "\n"
                        "    def _merge(self, arr, left, mid, right):\n"
                        "        left_part = arr[left:mid + 1]\n"
                        "        right_part = arr[mid + 1:right + 1]\n"
                        "        i = j = 0\n"
                        "        k = left\n"
                        "        while i < len(left_part) and j < len(right_part):\n"
                        "            if left_part[i] <= right_part[j]:\n"
                        "                arr[k] = left_part[i]\n"
                        "                i += 1\n"
                        "            else:\n"
                        "                arr[k] = right_part[j]\n"
                        "                j += 1\n"
                        "            k += 1\n"
                        "        while i < len(left_part):\n"
                        "            arr[k] = left_part[i]\n"
                        "            i += 1\n"
                        "            k += 1\n"
                        "        while j < len(right_part):\n"
                        "            arr[k] = right_part[j]\n"
                        "            j += 1\n"
                        "            k += 1\n"
                        "\n"
                        "\n"
                        "# Security example: sort event log timestamps\n"
                        "event_timestamps = [1620, 1500, 1800, 1430, 1700, 1550]\n"
                        "sorted_events = merge_sorter().sort(event_timestamps)\n"
                        "print('Event log sorted chronologically:')\n"
                        "print(sorted_events)"
                    ),
                    "note": None,
                },
                {
                    "heading": "Python Built-in Sorting — What to Use in Real Scripts",
                    "body": (
                        "In production Python you almost never implement a sorting "
                        "algorithm by hand. sorted() and list.sort() use Timsort — "
                        "a highly optimized merge+insertion hybrid. It's stable, O(n log n) "
                        "average/worst, and O(n) on nearly-sorted data (very common in logs).\n\n"
                        "The real skill is knowing how to use the key parameter to "
                        "sort by any attribute of complex objects."
                    ),
                    "code": (
                        "class security_alert:\n"
                        "    def __init__(self, name, severity, cvss_score, timestamp):\n"
                        "        self.name = name\n"
                        "        self.severity = severity\n"
                        "        self.cvss_score = cvss_score\n"
                        "        self.timestamp = timestamp\n"
                        "\n"
                        "    def __repr__(self):\n"
                        "        return f'{self.name}({self.severity}, cvss={self.cvss_score})'\n"
                        "\n"
                        "\n"
                        "alerts = [\n"
                        "    security_alert('brute-force',    'high',     7.5, 1003),\n"
                        "    security_alert('port-scan',      'low',      2.1, 1001),\n"
                        "    security_alert('malware-beacon', 'critical', 9.8, 1002),\n"
                        "    security_alert('sql-injection',  'high',     8.2, 1000),\n"
                        "    security_alert('weak-cipher',    'medium',   4.0, 1004),\n"
                        "]\n"
                        "\n"
                        "# Sort by CVSS score descending — highest risk first\n"
                        "by_risk = sorted(alerts, key=lambda a: a.cvss_score, reverse=True)\n"
                        "print('Alerts by CVSS risk (highest first):')\n"
                        "for a in by_risk:\n"
                        "    print(f'  cvss {a.cvss_score:4.1f}  {a.severity:8}  {a.name}')\n"
                        "\n"
                        "# Sort by timestamp to reconstruct the event timeline\n"
                        "by_time = sorted(alerts, key=lambda a: a.timestamp)\n"
                        "print('\\nAlert timeline:')\n"
                        "for a in by_time:\n"
                        "    print(f'  t={a.timestamp}  {a.name}')"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Vulnerability Triage Sorter",
                "instruction": (
                    "Given a list of vulnerabilities (each with a name, cvss_score, and "
                    "affected_hosts count), sort them two ways: first by cvss_score "
                    "descending, then by a combined risk_score (cvss_score * affected_hosts) "
                    "descending. Print both sorted lists and notice how the ranking changes "
                    "when host count is factored in."
                ),
                "starter_code": (
                    "class vulnerability:\n"
                    "    def __init__(self, name, cvss_score, affected_hosts):\n"
                    "        self.name = name\n"
                    "        self.cvss_score = cvss_score\n"
                    "        self.affected_hosts = affected_hosts\n"
                    "        self.risk_score = cvss_score * affected_hosts\n"
                    "\n"
                    "    def __repr__(self):\n"
                    "        return f'{self.name} (cvss={self.cvss_score}, hosts={self.affected_hosts}, risk={self.risk_score:.1f})'\n"
                    "\n"
                    "\n"
                    "vulns = [\n"
                    "    vulnerability('CVE-2025-1001 RCE',          9.8,  3),\n"
                    "    vulnerability('CVE-2025-1002 XSS',          6.1, 45),\n"
                    "    vulnerability('CVE-2025-1003 SQLi',         8.5, 12),\n"
                    "    vulnerability('CVE-2025-1004 weak-cipher',  4.3, 90),\n"
                    "    vulnerability('CVE-2025-1005 priv-esc',     7.8,  2),\n"
                    "]\n"
                    "\n"
                    "print('By CVSS score (pure severity):')\n"
                    "for v in sorted(vulns, key=lambda v: v.cvss_score, reverse=True):\n"
                    "    print(f'  {v}')\n"
                    "\n"
                    "print('\\nBy risk score (severity x affected hosts):')\n"
                    "for v in sorted(vulns, key=lambda v: v.risk_score, reverse=True):\n"
                    "    print(f'  {v}')"
                ),
            },
        },

        # ── Lesson 3 ─────────────────────────────────────────────────────────
        {
            "id": "pa-l3-security-scripting",
            "title": "Python Security Scripting — Bash to Python",
            "duration": "30 min",
            "objectives": [
                "Translate common bash audit patterns to Python using subprocess and pathlib",
                "Build a reusable OOP Auditor base class with ok/warn/fail counters",
                "Structure a multi-check security audit that prints a pass/warn/fail summary",
            ],
            "sections": [
                {
                    "heading": "Why Convert Bash to Python",
                    "body": (
                        "A 392-line bash security audit script (like arc-sec-audit) works, "
                        "but bash has real limitations: no native data structures, fragile "
                        "string parsing, hard to test, and no OOP. Converting to Python "
                        "gives you the same logic in a structure that's modular, testable, "
                        "and extendable — each check becomes its own function or class, "
                        "and shared state (counters, output helpers) lives in one base class.\n\n"
                        "The three main translation patterns are:\n"
                        "1. Shell commands → subprocess.run()\n"
                        "2. stat -c '%a' file → pathlib.Path.stat().st_mode\n"
                        "3. grep 'pattern' file → re.finditer() on file content"
                    ),
                    "code": (
                        "# Pattern 1: Shell command → subprocess.run()\n"
                        "# bash:   val=$(sysctl -n kernel.randomize_va_space)\n"
                        "# python:\n"
                        "import subprocess\n"
                        "\n"
                        "def run_cmd(cmd_list, timeout=10):\n"
                        "    try:\n"
                        "        result = subprocess.run(\n"
                        "            cmd_list, capture_output=True, text=True, timeout=timeout\n"
                        "        )\n"
                        "        return result.stdout.strip()\n"
                        "    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):\n"
                        "        return ''\n"
                        "\n"
                        "\n"
                        "# Pattern 2: File permissions → pathlib\n"
                        "# bash:   actual=$(stat -c '%a' /etc/shadow)\n"
                        "# python:\n"
                        "from pathlib import Path\n"
                        "\n"
                        "def get_perms(path_str):\n"
                        "    p = Path(path_str)\n"
                        "    if not p.exists():\n"
                        "        return None\n"
                        "    return oct(p.stat().st_mode)[-3:]\n"
                        "\n"
                        "\n"
                        "# Pattern 3: grep on file → re\n"
                        "# bash:   grep -rih '^PermitRootLogin' /etc/ssh/sshd_config | tail -1\n"
                        "# python:\n"
                        "import re\n"
                        "\n"
                        "def grep_file(filepath, pattern):\n"
                        "    p = Path(filepath)\n"
                        "    if not p.exists():\n"
                        "        return None\n"
                        "    matches = re.findall(\n"
                        "        pattern, p.read_text(errors='replace'), re.IGNORECASE\n"
                        "    )\n"
                        "    return matches[-1] if matches else None\n"
                        "\n"
                        "\n"
                        "# Show the patterns in action (these work on this machine)\n"
                        "perms = get_perms('/etc/hostname')\n"
                        "print(f'/etc/hostname permissions: {perms}')\n"
                        "\n"
                        "hostname = run_cmd(['hostname'])\n"
                        "print(f'Hostname: {hostname}')"
                    ),
                    "note": None,
                },
                {
                    "heading": "The OOP Auditor Base Class",
                    "body": (
                        "arc-sec-audit structures its nine check modules around a shared "
                        "Auditor base class. The base class holds: three counters "
                        "(passed/warnings/failed), output helpers (ok/warn/fail that "
                        "both print and increment the right counter), a subprocess wrapper "
                        "(run()), and helper methods for the two most common check patterns "
                        "(sysctl_chk and perm_chk).\n\n"
                        "Each check module is then just a function check(auditor) that "
                        "calls those helpers — clean, flat, testable."
                    ),
                    "code": (
                        "class auditor:\n"
                        "    def __init__(self):\n"
                        "        self.passed = 0\n"
                        "        self.warnings = 0\n"
                        "        self.failed = 0\n"
                        "\n"
                        "    def ok(self, msg):\n"
                        "        print(f'  PASS  {msg}')\n"
                        "        self.passed += 1\n"
                        "\n"
                        "    def warn(self, msg):\n"
                        "        print(f'  WARN  {msg}')\n"
                        "        self.warnings += 1\n"
                        "\n"
                        "    def fail(self, msg):\n"
                        "        print(f'  FAIL  {msg}')\n"
                        "        self.failed += 1\n"
                        "\n"
                        "    def hdr(self, msg):\n"
                        "        print(f'\\n--- {msg} ---')\n"
                        "\n"
                        "    def run(self, cmd, timeout=10):\n"
                        "        import subprocess\n"
                        "        try:\n"
                        "            result = subprocess.run(\n"
                        "                cmd, capture_output=True, text=True, timeout=timeout\n"
                        "            )\n"
                        "            return result.stdout.strip()\n"
                        "        except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):\n"
                        "            return ''\n"
                        "\n"
                        "    def perm_chk(self, path, want):\n"
                        "        from pathlib import Path\n"
                        "        p = Path(path)\n"
                        "        if not p.exists():\n"
                        "            self.warn(f'{path} not found')\n"
                        "            return\n"
                        "        actual = oct(p.stat().st_mode)[-3:]\n"
                        "        if actual == want:\n"
                        "            self.ok(f'{path} permissions {actual}')\n"
                        "        else:\n"
                        "            self.warn(f'{path} permissions {actual} (want {want})')\n"
                        "\n"
                        "    def summary(self):\n"
                        "        total = self.passed + self.warnings + self.failed\n"
                        "        print(f'\\nResults: {self.passed} passed, {self.warnings} warnings, {self.failed} failed / {total} total')\n"
                        "\n"
                        "\n"
                        "# Use it\n"
                        "a = auditor()\n"
                        "\n"
                        "a.hdr('Permission Checks')\n"
                        "a.perm_chk('/etc/hostname', '644')\n"
                        "a.perm_chk('/etc/hosts',    '644')\n"
                        "a.perm_chk('/etc/shadow',   '640')\n"
                        "\n"
                        "a.summary()"
                    ),
                    "note": (
                        "/etc/shadow is typically owned by root:shadow with mode 640. "
                        "If this runs as a non-root user, the stat() call may raise "
                        "PermissionError — the perm_chk helper handles it gracefully."
                    ),
                },
                {
                    "heading": "The Nine Check Categories — arc-sec-audit Structure",
                    "body": (
                        "arc-sec-audit organizes its 9 checks as separate modules, each "
                        "exporting a single function check(auditor). The entry point "
                        "calls them in sequence and prints the final summary.\n\n"
                        "The nine categories:\n"
                        "ssh — PermitRootLogin, PasswordAuthentication, X11Forwarding\n"
                        "kernel — ASLR, dmesg_restrict, kptr_restrict, syncookies\n"
                        "perms — passwd, shadow, sudoers, /root, SSH host keys\n"
                        "suid — SUID binaries vs known-good baseline\n"
                        "world-write — world-writable files in /etc /home /usr /var\n"
                        "sudoers — NOPASSWD:ALL entries outside whitelisted files\n"
                        "services — TCP listeners localhost-bound vs network-exposed\n"
                        "packages — pending security updates + debsecan CVE check\n"
                        "system — root account lock, AppArmor, core dumps, unattended-upgrades"
                    ),
                    "code": (
                        "class auditor:\n"
                        "    def __init__(self):\n"
                        "        self.passed = 0\n"
                        "        self.warnings = 0\n"
                        "        self.failed = 0\n"
                        "\n"
                        "    def ok(self, msg):   print(f'  PASS  {msg}'); self.passed += 1\n"
                        "    def warn(self, msg): print(f'  WARN  {msg}'); self.warnings += 1\n"
                        "    def fail(self, msg): print(f'  FAIL  {msg}'); self.failed += 1\n"
                        "    def hdr(self, msg):  print(f'\\n--- {msg} ---')\n"
                        "\n"
                        "    def summary(self):\n"
                        "        total = self.passed + self.warnings + self.failed\n"
                        "        print(f'\\nResults: {self.passed}P / {self.warnings}W / {self.failed}F / {total} total')\n"
                        "\n"
                        "\n"
                        "# Simulated check modules — mirrors the arc-sec-audit structure\n"
                        "\n"
                        "def check_ssh(a, sshd_config_lines):\n"
                        "    a.hdr('SSH Configuration')\n"
                        "    settings = {}\n"
                        "    for line in sshd_config_lines:\n"
                        "        if line.strip() and not line.startswith('#'):\n"
                        "            parts = line.split()\n"
                        "            if len(parts) >= 2:\n"
                        "                settings[parts[0].lower()] = parts[1].lower()\n"
                        "\n"
                        "    val = settings.get('permitrootlogin', 'yes')\n"
                        "    if val in ('no', 'prohibit-password'):\n"
                        "        a.ok(f'PermitRootLogin {val}')\n"
                        "    else:\n"
                        "        a.fail(f'PermitRootLogin {val} (want no)')\n"
                        "\n"
                        "    val = settings.get('passwordauthentication', 'yes')\n"
                        "    if val == 'no':\n"
                        "        a.ok('PasswordAuthentication no')\n"
                        "    else:\n"
                        "        a.warn('PasswordAuthentication yes — consider key-only auth')\n"
                        "\n"
                        "\n"
                        "def check_system(a, root_locked, apparmor_active, core_dumps_disabled):\n"
                        "    a.hdr('System Integrity')\n"
                        "    if root_locked:\n"
                        "        a.ok('root account locked')\n"
                        "    else:\n"
                        "        a.fail('root account has a valid login shell')\n"
                        "\n"
                        "    if apparmor_active:\n"
                        "        a.ok('AppArmor active')\n"
                        "    else:\n"
                        "        a.warn('AppArmor not enforcing')\n"
                        "\n"
                        "    if core_dumps_disabled:\n"
                        "        a.ok('core dumps disabled')\n"
                        "    else:\n"
                        "        a.warn('core dumps enabled — may leak sensitive memory')\n"
                        "\n"
                        "\n"
                        "a = auditor()\n"
                        "\n"
                        "sshd_config = [\n"
                        "    'PermitRootLogin no',\n"
                        "    'PasswordAuthentication yes',\n"
                        "    'X11Forwarding no',\n"
                        "]\n"
                        "check_ssh(a, sshd_config)\n"
                        "check_system(a, root_locked=True, apparmor_active=True, core_dumps_disabled=False)\n"
                        "\n"
                        "a.summary()"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a Mini Hardening Auditor",
                "instruction": (
                    "Using the auditor base class, write two check functions: "
                    "check_kernel(a, sysctl_values) which verifies that "
                    "kernel.randomize_va_space is 2 and kernel.dmesg_restrict is 1, "
                    "and check_ssh(a, sshd_lines) which verifies PermitRootLogin is no "
                    "and X11Forwarding is no. Run both and print the summary."
                ),
                "starter_code": (
                    "class auditor:\n"
                    "    def __init__(self):\n"
                    "        self.passed = 0\n"
                    "        self.warnings = 0\n"
                    "        self.failed = 0\n"
                    "\n"
                    "    def ok(self, msg):   print(f'  PASS  {msg}'); self.passed += 1\n"
                    "    def warn(self, msg): print(f'  WARN  {msg}'); self.warnings += 1\n"
                    "    def fail(self, msg): print(f'  FAIL  {msg}'); self.failed += 1\n"
                    "    def hdr(self, msg):  print(f'\\n--- {msg} ---')\n"
                    "\n"
                    "    def summary(self):\n"
                    "        total = self.passed + self.warnings + self.failed\n"
                    "        print(f'\\nResults: {self.passed}P / {self.warnings}W / {self.failed}F / {total} total')\n"
                    "\n"
                    "\n"
                    "def check_kernel(a, sysctl_values):\n"
                    "    a.hdr('Kernel Parameters')\n"
                    "    checks = [\n"
                    "        ('kernel.randomize_va_space', '2', 'ASLR disabled'),\n"
                    "        ('kernel.dmesg_restrict',     '1', 'dmesg readable by non-root'),\n"
                    "    ]\n"
                    "    for key, want, fail_msg in checks:\n"
                    "        actual = sysctl_values.get(key)\n"
                    "        if actual is None:\n"
                    "            a.warn(f'{key} not available on this kernel')\n"
                    "        elif actual == want:\n"
                    "            a.ok(f'{key} = {actual}')\n"
                    "        else:\n"
                    "            a.fail(f'{key} = {actual} (want {want}) -- {fail_msg}')\n"
                    "\n"
                    "\n"
                    "def check_ssh(a, sshd_lines):\n"
                    "    a.hdr('SSH Hardening')\n"
                    "    settings = {}\n"
                    "    for line in sshd_lines:\n"
                    "        parts = line.split()\n"
                    "        if len(parts) >= 2:\n"
                    "            settings[parts[0].lower()] = parts[1].lower()\n"
                    "\n"
                    "    val = settings.get('permitrootlogin', 'yes')\n"
                    "    if val in ('no', 'prohibit-password'):\n"
                    "        a.ok(f'PermitRootLogin {val}')\n"
                    "    else:\n"
                    "        a.fail(f'PermitRootLogin {val} -- root SSH login allowed')\n"
                    "\n"
                    "    val = settings.get('x11forwarding', 'yes')\n"
                    "    if val == 'no':\n"
                    "        a.ok('X11Forwarding no')\n"
                    "    else:\n"
                    "        a.warn('X11Forwarding yes -- GUI forwarding enabled')\n"
                    "\n"
                    "\n"
                    "a = auditor()\n"
                    "\n"
                    "sysctl = {\n"
                    "    'kernel.randomize_va_space': '2',\n"
                    "    'kernel.dmesg_restrict': '0',\n"
                    "}\n"
                    "\n"
                    "sshd = [\n"
                    "    'PermitRootLogin no',\n"
                    "    'X11Forwarding yes',\n"
                    "    'PasswordAuthentication no',\n"
                    "]\n"
                    "\n"
                    "check_kernel(a, sysctl)\n"
                    "check_ssh(a, sshd)\n"
                    "a.summary()"
                ),
            },
        },
    ],
}
