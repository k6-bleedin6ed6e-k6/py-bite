# ─────────────────────────────────────────────────────────────────────────────
# Network Fundamentals chapter — Managing Networks · Common Commands · SNMP ·
# NetFlow · IP SLA
# Drop this dict into the CHAPTERS list in app/content.py (see header there).
# Matches your existing chapter/lesson structure exactly (same shape as
# ch-network-automation: id/number/title/subtitle/description/lessons[]).
# ─────────────────────────────────────────────────────────────────────────────

NETWORK_FUNDAMENTALS_CHAPTER = {
    "id": "ch-network-fundamentals",
    "number": 8,
    "title": "Network Management Fundamentals",
    "subtitle": "Managing Networks · Common Commands · SNMP · NetFlow · IP SLA",
    "description": (
        "Five building blocks of day-one network management. Each lesson "
        "pairs the real Cisco IOS commands you'll actually type with a "
        "small Python simulation of the same idea, so you can practice the "
        "logic safely with zero lab gear."
    ),
    "lessons": [

        # ── Lesson 1 ─────────────────────────────────────────────────────────
        {
            "id": "nf-l1-managing-networks",
            "title": "Managing Networks — The FCAPS Model",
            "duration": "15 min",
            "objectives": [
                "Name the five FCAPS categories of network management",
                "Sort a real-world scenario into the right FCAPS bucket",
                "Build a tiny fault-checker over a list of devices",
            ],
            "sections": [
                {
                    "heading": "The Five Buckets",
                    "body": (
                        "Everything a network admin does falls into one of five "
                        "buckets, FCAPS: Fault (detect/fix problems), Configuration "
                        "(keep settings correct), Accounting (track usage), "
                        "Performance (keep it fast), Security (keep it safe). "
                        "When you're not sure what 'kind' of task something is, "
                        "ask: which of these five is it protecting?"
                    ),
                    "code": None,
                    "note": None,
                },
                {
                    "heading": "Practice — A Tiny Fault Checker",
                    "body": (
                        "Real fault management means scanning device status and "
                        "flagging anything down. Here's the same idea in plain "
                        "Python over a list of device dictionaries."
                    ),
                    "code": (
                        "devices = [\n"
                        "    {\"name\": \"core-sw1\", \"status\": \"up\"},\n"
                        "    {\"name\": \"edge-rtr2\", \"status\": \"down\"},\n"
                        "    {\"name\": \"access-sw3\", \"status\": \"up\"},\n"
                        "]\n"
                        "\n"
                        "def find_faults(devices):\n"
                        "    return [d[\"name\"] for d in devices if d[\"status\"] == \"down\"]\n"
                        "\n"
                        "print(\"Devices down:\", find_faults(devices))"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a FCAPS Sorter",
                "instruction": (
                    "Write a function classify_task(task_text) that looks at a "
                    "short string describing an admin task and returns which "
                    "FCAPS letter it belongs to: 'F', 'C', 'A', 'P', or 'S'. "
                    "Use simple keyword matching (e.g. 'down', 'crash', 'outage' "
                    "-> 'F'; 'password', 'firewall', 'unauthorized' -> 'S'; "
                    "'slow', 'latency', 'bandwidth' -> 'P'; 'config', 'backup', "
                    "'template' -> 'C'; 'usage', 'billing', 'report' -> 'A'). "
                    "Test it against the sample_tasks list."
                ),
                "starter_code": (
                    "sample_tasks = [\n"
                    "    \"Switch port 0/3 went down at 2am\",\n"
                    "    \"Someone tried an unauthorized login on the firewall\",\n"
                    "    \"WAN link latency spiked during business hours\",\n"
                    "    \"Pushed a new VLAN config template to all access switches\",\n"
                    "    \"Generate monthly bandwidth usage report for billing\",\n"
                    "]\n"
                    "\n"
                    "def classify_task(task_text):\n"
                    "    task_text = task_text.lower()\n"
                    "    rules = {\n"
                    "        \"F\": [\"down\", \"crash\", \"outage\"],\n"
                    "        \"S\": [\"password\", \"firewall\", \"unauthorized\"],\n"
                    "        \"P\": [\"slow\", \"latency\", \"bandwidth\"],\n"
                    "        \"C\": [\"config\", \"backup\", \"template\"],\n"
                    "        \"A\": [\"usage\", \"billing\", \"report\"],\n"
                    "    }\n"
                    "    for letter, keywords in rules.items():\n"
                    "        if any(keyword in task_text for keyword in keywords):\n"
                    "            return letter\n"
                    "    return \"?\"\n"
                    "\n"
                    "for task in sample_tasks:\n"
                    "    print(f\"{classify_task(task)} -> {task}\")"
                ),
            },
        },

        # ── Lesson 2 ─────────────────────────────────────────────────────────
        {
            "id": "nf-l2-common-commands",
            "title": "Common IOS Commands — The Daily Toolkit",
            "duration": "15 min",
            "objectives": [
                "Recognize the handful of commands you'll run constantly",
                "Know what each one is actually telling you",
                "Build a simulated CLI command dispatcher",
            ],
            "sections": [
                {
                    "heading": "The Commands You'll Live In",
                    "body": (
                        "show ip interface brief is the one you'll run a hundred "
                        "times a day -- quick status of every interface. Add to "
                        "that: show running-config (active settings), show version "
                        "(IOS + hardware info), ping / traceroute (connectivity "
                        "tests), show cdp neighbors (what's directly connected), "
                        "and copy running-config startup-config (SAVE your work -- "
                        "this is the one beginners forget and lose everything on "
                        "reboot)."
                    ),
                    "code": (
                        "enable\n"
                        "configure terminal\n"
                        "show running-config\n"
                        "show ip interface brief\n"
                        "show version\n"
                        "copy running-config startup-config\n"
                        "ping 8.8.8.8\n"
                        "traceroute 8.8.8.8\n"
                        "show cdp neighbors"
                    ),
                    "note": "This is real Cisco IOS syntax -- not Python. You'd type this in a terminal/console session, not 'Run' it here.",
                },
                {
                    "heading": "Practice — Simulated CLI",
                    "body": (
                        "Here's the same idea as a tiny Python dispatcher: a "
                        "dictionary of canned command outputs, like a simulated "
                        "device session."
                    ),
                    "code": (
                        "CANNED_OUTPUT = {\n"
                        "    \"show version\": \"Cisco IOS Software, Version 15.2(7)E3\",\n"
                        "    \"show ip interface brief\": \"Gig0/0  up    Gig0/1  down\",\n"
                        "}\n"
                        "\n"
                        "def run_command(cmd):\n"
                        "    return CANNED_OUTPUT.get(cmd, f\"% Invalid input detected: {cmd}\")\n"
                        "\n"
                        "print(run_command(\"show version\"))\n"
                        "print(run_command(\"show ip interface brief\"))\n"
                        "print(run_command(\"reload\"))"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a Mini CLI Session",
                "instruction": (
                    "Build a class mini_cli_session with a CANNED_OUTPUT lookup "
                    "table (at least 4 commands) and a run(command) method. Add a "
                    "history list that records every command run, and a "
                    "show_history() method that prints them in order."
                ),
                "starter_code": (
                    "class mini_cli_session:\n"
                    "    CANNED_OUTPUT = {\n"
                    "        \"show version\": \"Cisco IOS Software, Version 15.2(7)E3\",\n"
                    "        \"show ip interface brief\": \"Gig0/0  up    Gig0/1  down\",\n"
                    "        \"show cdp neighbors\": \"core-sw1.local  Gig0/1  Switch\",\n"
                    "        \"show running-config\": \"hostname edge-rtr2\\nip routing\",\n"
                    "    }\n"
                    "\n"
                    "    def __init__(self):\n"
                    "        self.history = []\n"
                    "\n"
                    "    def run(self, command):\n"
                    "        self.history.append(command)\n"
                    "        return self.CANNED_OUTPUT.get(command, f\"% Invalid input detected: {command}\")\n"
                    "\n"
                    "    def show_history(self):\n"
                    "        for i, cmd in enumerate(self.history, start=1):\n"
                    "            print(f\"{i}. {cmd}\")\n"
                    "\n"
                    "\n"
                    "session = mini_cli_session()\n"
                    "print(session.run(\"show version\"))\n"
                    "print(session.run(\"show ip interface brief\"))\n"
                    "print(session.run(\"reload\"))\n"
                    "print(\"--- history ---\")\n"
                    "session.show_history()"
                ),
            },
        },

        # ── Lesson 3 ─────────────────────────────────────────────────────────
        {
            "id": "nf-l3-snmp",
            "title": "SNMP — Polling Devices for Stats",
            "duration": "20 min",
            "objectives": [
                "Explain what SNMP is used for",
                "Know the key difference between SNMPv2c and SNMPv3",
                "Build a simulated OID lookup + security checker",
            ],
            "sections": [
                {
                    "heading": "SNMPv2c vs SNMPv3",
                    "body": (
                        "SNMP lets a central server (SolarWinds, Zabbix, PRTG) poll "
                        "devices for stats like CPU and interface traffic. SNMPv2c "
                        "is simple but sends its 'community string' password in "
                        "plain text -- anyone sniffing the wire can read it. "
                        "SNMPv3 adds real authentication and encryption and is "
                        "what you should use in production."
                    ),
                    "code": (
                        "! SNMPv2c -- plaintext community string, avoid in production\n"
                        "snmp-server community MyReadOnlyString RO\n"
                        "snmp-server location server-room-1\n"
                        "\n"
                        "! SNMPv3 -- authenticated + encrypted\n"
                        "snmp-server group ADMINGROUP v3 priv\n"
                        "snmp-server user netadmin ADMINGROUP v3 auth sha MyAuthPass123 priv aes 128 MyPrivPass123"
                    ),
                    "note": "Real Cisco IOS syntax -- reference only, not runnable Python.",
                },
                {
                    "heading": "Practice — Simulated OID Poll",
                    "body": (
                        "SNMP works by polling OIDs (object identifiers) -- think "
                        "of them as addresses for specific stats. Here's a tiny "
                        "simulated poller."
                    ),
                    "code": (
                        "OID_TABLE = {\n"
                        "    \"1.3.6.1.2.1.1.5.0\": \"core-sw1\",       # sysName\n"
                        "    \"1.3.6.1.2.1.1.3.0\": \"19 days, 3:41\",  # sysUptime\n"
                        "}\n"
                        "\n"
                        "def snmp_get(oid):\n"
                        "    return OID_TABLE.get(oid, \"No Such Object\")\n"
                        "\n"
                        "print(snmp_get(\"1.3.6.1.2.1.1.5.0\"))"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build an SNMP Security Auditor",
                "instruction": (
                    "Write a function audit_snmp_config(config) that takes a dict "
                    "describing a device's SNMP setup and returns a list of "
                    "warning strings. Flag it if version is 'v2c' ('Plaintext "
                    "community string -- upgrade to SNMPv3'), if version is 'v3' "
                    "but encryption is False ('SNMPv3 without privacy is no "
                    "better than v2c'), and if community is 'public' or 'private' "
                    "('Default community string in use -- change it immediately')."
                ),
                "starter_code": (
                    "configs = [\n"
                    "    {\"hostname\": \"core-sw1\", \"version\": \"v2c\", \"community\": \"public\"},\n"
                    "    {\"hostname\": \"edge-rtr2\", \"version\": \"v3\", \"encryption\": False},\n"
                    "    {\"hostname\": \"access-sw3\", \"version\": \"v3\", \"encryption\": True},\n"
                    "]\n"
                    "\n"
                    "def audit_snmp_config(config):\n"
                    "    warnings = []\n"
                    "    if config.get(\"version\") == \"v2c\":\n"
                    "        warnings.append(\"Plaintext community string -- upgrade to SNMPv3\")\n"
                    "    if config.get(\"version\") == \"v3\" and not config.get(\"encryption\", False):\n"
                    "        warnings.append(\"SNMPv3 without privacy is no better than v2c\")\n"
                    "    if config.get(\"community\") in (\"public\", \"private\"):\n"
                    "        warnings.append(\"Default community string in use -- change it immediately\")\n"
                    "    return warnings\n"
                    "\n"
                    "for config in configs:\n"
                    "    issues = audit_snmp_config(config)\n"
                    "    print(config[\"hostname\"], \"->\", issues if issues else \"OK\")"
                ),
            },
        },

        # ── Lesson 4 ─────────────────────────────────────────────────────────
        {
            "id": "nf-l4-netflow",
            "title": "NetFlow — Who Talked to Who",
            "duration": "20 min",
            "objectives": [
                "Explain what NetFlow records (and what it does NOT record)",
                "Configure flow export at a conceptual level",
                "Find the top talker in a list of flow records",
            ],
            "sections": [
                {
                    "heading": "Metadata, Not Content",
                    "body": (
                        "NetFlow records traffic metadata: source, destination, "
                        "ports, protocol, and byte counts -- not the actual packet "
                        "content. It's how you spot 'this host is suddenly sending "
                        "10x its normal traffic' without ever inspecting payloads. "
                        "Genuinely useful for SOC/blue-team traffic analysis too."
                    ),
                    "code": (
                        "interface GigabitEthernet0/1\n"
                        " ip flow ingress\n"
                        " ip flow egress\n"
                        "\n"
                        "ip flow-export destination 192.168.1.100 2055\n"
                        "ip flow-export version 9"
                    ),
                    "note": "Real Cisco IOS syntax -- reference only.",
                },
                {
                    "heading": "Practice — Find the Top Talker",
                    "body": "A simulated batch of flow records and a quick scan for the heaviest sender.",
                    "code": (
                        "flows = [\n"
                        "    {\"src\": \"10.0.0.5\", \"dst\": \"8.8.8.8\", \"bytes\": 4096},\n"
                        "    {\"src\": \"10.0.0.7\", \"dst\": \"1.1.1.1\", \"bytes\": 512000},\n"
                        "    {\"src\": \"10.0.0.5\", \"dst\": \"8.8.4.4\", \"bytes\": 2048},\n"
                        "]\n"
                        "\n"
                        "top = max(flows, key=lambda f: f[\"bytes\"])\n"
                        "print(f\"Top talker: {top['src']} sent {top['bytes']} bytes\")"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Aggregate Flow Data Per Host",
                "instruction": (
                    "Write a function total_bytes_by_source(flows) that returns a "
                    "dict mapping each source IP to its total bytes sent across "
                    "all flow records. Then print the result sorted from highest "
                    "to lowest total."
                ),
                "starter_code": (
                    "flows = [\n"
                    "    {\"src\": \"10.0.0.5\", \"dst\": \"8.8.8.8\", \"bytes\": 4096},\n"
                    "    {\"src\": \"10.0.0.7\", \"dst\": \"1.1.1.1\", \"bytes\": 512000},\n"
                    "    {\"src\": \"10.0.0.5\", \"dst\": \"8.8.4.4\", \"bytes\": 2048},\n"
                    "    {\"src\": \"10.0.0.7\", \"dst\": \"9.9.9.9\", \"bytes\": 1024},\n"
                    "]\n"
                    "\n"
                    "def total_bytes_by_source(flows):\n"
                    "    totals = {}\n"
                    "    for flow in flows:\n"
                    "        totals[flow[\"src\"]] = totals.get(flow[\"src\"], 0) + flow[\"bytes\"]\n"
                    "    return totals\n"
                    "\n"
                    "totals = total_bytes_by_source(flows)\n"
                    "for src, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):\n"
                    "    print(f\"{src}: {total} bytes\")"
                ),
            },
        },

        # ── Lesson 5 ─────────────────────────────────────────────────────────
        {
            "id": "nf-l5-ip-sla",
            "title": "IP SLA — Proactive Health Checks",
            "duration": "15 min",
            "objectives": [
                "Explain why IP SLA beats waiting for a user complaint",
                "Configure a basic ICMP echo SLA probe",
                "Build a latency tracker that flags SLA violations",
            ],
            "sections": [
                {
                    "heading": "Catch It Before Users Do",
                    "body": (
                        "IP SLA schedules synthetic tests -- automated pings/traces "
                        "the router runs on its own -- so you find out latency to "
                        "the data center spiked at 30 seconds, not when a user "
                        "calls the help desk an hour later."
                    ),
                    "code": (
                        "ip sla 1\n"
                        " icmp-echo 192.168.1.1\n"
                        " frequency 30\n"
                        "ip sla schedule 1 life forever start-time now\n"
                        "\n"
                        "show ip sla statistics"
                    ),
                    "note": "Real Cisco IOS syntax -- reference only.",
                },
                {
                    "heading": "Practice — Latency Tracker",
                    "body": "A simulated batch of probe results and a basic threshold check.",
                    "code": (
                        "probe_results_ms = [12, 14, 13, 95, 11, 13]\n"
                        "THRESHOLD_MS = 50\n"
                        "\n"
                        "violations = [r for r in probe_results_ms if r > THRESHOLD_MS]\n"
                        "print(f\"Violations: {violations}\")"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build an SLA Monitor",
                "instruction": (
                    "Write a function check_sla(probe_results_ms, threshold_ms) "
                    "that returns a dict with keys 'average', 'max', and "
                    "'violations' (count of readings above threshold). Then run "
                    "it against the sample data and print a one-line health "
                    "summary."
                ),
                "starter_code": (
                    "probe_results_ms = [12, 14, 13, 95, 11, 13, 120, 14]\n"
                    "\n"
                    "def check_sla(probe_results_ms, threshold_ms):\n"
                    "    average = sum(probe_results_ms) / len(probe_results_ms)\n"
                    "    return {\n"
                    "        \"average\": round(average, 1),\n"
                    "        \"max\": max(probe_results_ms),\n"
                    "        \"violations\": sum(1 for r in probe_results_ms if r > threshold_ms),\n"
                    "    }\n"
                    "\n"
                    "result = check_sla(probe_results_ms, threshold_ms=50)\n"
                    "status = \"DEGRADED\" if result[\"violations\"] > 0 else \"HEALTHY\"\n"
                    "print(f\"avg={result['average']}ms max={result['max']}ms violations={result['violations']} -> {status}\")"
                ),
            },
        },
    ],
}
