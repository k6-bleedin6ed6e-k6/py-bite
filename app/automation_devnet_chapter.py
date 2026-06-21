# ─────────────────────────────────────────────────────────────────────────────
# Automation & DevNet chapter — JSON/XML · Python for Networking ·
# Orchestration · Cisco DNA Center · Study Strategies
# Drop this dict into the CHAPTERS list in app/content.py (see header there).
# Pairs naturally with ch-network-automation (Paramiko/Netmiko/Ansible/
# NAPALM/Telnet) -- this chapter covers the layer above those drivers.
# ─────────────────────────────────────────────────────────────────────────────

AUTOMATION_DEVNET_CHAPTER = {
    "id": "ch-automation-devnet",
    "number": 10,
    "title": "Automation, Data & DNA Center",
    "subtitle": "JSON/XML · Python for Networking · Orchestration · DNA Center · Study Tips",
    "description": (
        "The layer above individual SSH drivers: how data moves (JSON/XML), "
        "how Python loops over many devices at once, how orchestration "
        "chains tasks together, and how Cisco DNA Center ties it all into "
        "one dashboard. Closes with exam-ready study strategies."
    ),
    "lessons": [

        # ── Lesson 1 ─────────────────────────────────────────────────────────
        {
            "id": "ad-l1-json-xml",
            "title": "JSON and XML — How Devices Talk Data",
            "duration": "15 min",
            "objectives": [
                "Read and write basic JSON in Python",
                "Parse a simple XML string",
                "Know when you'll see each format in the real world",
            ],
            "sections": [
                {
                    "heading": "JSON: Lighter, Modern, Everywhere",
                    "body": (
                        "Most modern REST APIs (including Cisco DNA Center) speak "
                        "JSON -- lightweight, human-readable, maps directly onto "
                        "Python dicts and lists. XML is older and heavier but "
                        "still shows up in legacy systems and NETCONF."
                    ),
                    "code": (
                        "import json\n"
                        "\n"
                        "data = {\n"
                        "    \"hostname\": \"router1\",\n"
                        "    \"interfaces\": [\n"
                        "        {\"name\": \"Gig0/0\", \"status\": \"up\"},\n"
                        "        {\"name\": \"Gig0/1\", \"status\": \"down\"},\n"
                        "    ],\n"
                        "}\n"
                        "\n"
                        "json_string = json.dumps(data, indent=2)\n"
                        "print(json_string)\n"
                        "\n"
                        "parsed = json.loads(json_string)\n"
                        "print(parsed[\"interfaces\"][0][\"status\"])"
                    ),
                    "note": None,
                },
                {
                    "heading": "XML — Still Around in NETCONF",
                    "body": "Same data, XML-style, parsed with the standard library.",
                    "code": (
                        "import xml.etree.ElementTree as ET\n"
                        "\n"
                        "xml_string = \"\"\"<device>\n"
                        "  <hostname>router1</hostname>\n"
                        "  <interface name=\"Gig0/0\">up</interface>\n"
                        "</device>\"\"\"\n"
                        "\n"
                        "root = ET.fromstring(xml_string)\n"
                        "print(root.find(\"hostname\").text)\n"
                        "print(root.find(\"interface\").attrib[\"name\"])"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Convert and Filter Device Inventory",
                "instruction": (
                    "Given a JSON string of multiple devices, parse it, filter "
                    "to only devices with status 'down', and print a clean "
                    "report line for each one. Then do the same for the XML "
                    "version below using ElementTree."
                ),
                "starter_code": (
                    "import json\n"
                    "import xml.etree.ElementTree as ET\n"
                    "\n"
                    "json_inventory = json.dumps({\n"
                    "    \"devices\": [\n"
                    "        {\"name\": \"core-sw1\", \"status\": \"up\"},\n"
                    "        {\"name\": \"edge-rtr2\", \"status\": \"down\"},\n"
                    "        {\"name\": \"access-sw3\", \"status\": \"down\"},\n"
                    "    ]\n"
                    "})\n"
                    "\n"
                    "data = json.loads(json_inventory)\n"
                    "print(\"--- JSON: down devices ---\")\n"
                    "for device in data[\"devices\"]:\n"
                    "    if device[\"status\"] == \"down\":\n"
                    "        print(f\"  {device['name']} is DOWN\")\n"
                    "\n"
                    "xml_inventory = \"\"\"<devices>\n"
                    "    <device name=\"core-sw1\" status=\"up\"/>\n"
                    "    <device name=\"edge-rtr2\" status=\"down\"/>\n"
                    "</devices>\"\"\"\n"
                    "\n"
                    "root = ET.fromstring(xml_inventory)\n"
                    "print(\"--- XML: down devices ---\")\n"
                    "for device in root.findall(\"device\"):\n"
                    "    if device.attrib[\"status\"] == \"down\":\n"
                    "        print(f\"  {device.attrib['name']} is DOWN\")"
                ),
            },
        },

        # ── Lesson 2 ─────────────────────────────────────────────────────────
        {
            "id": "ad-l2-python-networking",
            "title": "Python for Networking — Looping Over Devices",
            "duration": "20 min",
            "objectives": [
                "Build a list of device connection dicts",
                "Loop over devices collecting results into one report",
                "Handle a failure in one device without crashing the whole run",
            ],
            "sections": [
                {
                    "heading": "The Pattern That Matters Most",
                    "body": (
                        "You don't need to be a software engineer for this -- you "
                        "need enough Python to connect, send a command, parse the "
                        "result, and loop over a list of devices. This pattern is "
                        "literally how you check 50 routers in 30 seconds instead "
                        "of 50 manual logins."
                    ),
                    "code": (
                        "devices = [\n"
                        "    {\"host\": \"192.168.1.1\", \"name\": \"core-sw1\"},\n"
                        "    {\"host\": \"192.168.1.2\", \"name\": \"edge-rtr2\"},\n"
                        "]\n"
                        "\n"
                        "def fake_send_command(host, command):\n"
                        "    # stands in for a real Netmiko connection.send_command()\n"
                        "    return f\"output of '{command}' from {host}\"\n"
                        "\n"
                        "for device in devices:\n"
                        "    result = fake_send_command(device[\"host\"], \"show version\")\n"
                        "    print(f\"{device['name']}: {result}\")"
                    ),
                    "note": "In a real driver this would be Netmiko's ConnectHandler + send_command -- see ch-network-automation for the full real-driver version.",
                },
            ],
            "exercise": {
                "title": "Build a Resilient Multi-Device Runner",
                "instruction": (
                    "Write a function run_on_all(devices, command, runner) that "
                    "loops over devices, calls runner(device, command), and "
                    "collects results into a dict {device_name: result}. If "
                    "runner() raises an exception for one device, catch it, "
                    "store the error message instead of crashing, and continue "
                    "to the next device."
                ),
                "starter_code": (
                    "devices = [\n"
                    "    {\"host\": \"192.168.1.1\", \"name\": \"core-sw1\"},\n"
                    "    {\"host\": \"192.168.1.2\", \"name\": \"edge-rtr2\"},\n"
                    "    {\"host\": \"192.168.1.3\", \"name\": \"unreachable-sw\"},\n"
                    "]\n"
                    "\n"
                    "def flaky_runner(device, command):\n"
                    "    if device[\"name\"] == \"unreachable-sw\":\n"
                    "        raise TimeoutError(\"connection timed out\")\n"
                    "    return f\"output of '{command}' from {device['host']}\"\n"
                    "\n"
                    "def run_on_all(devices, command, runner):\n"
                    "    results = {}\n"
                    "    for device in devices:\n"
                    "        try:\n"
                    "            results[device[\"name\"]] = runner(device, command)\n"
                    "        except Exception as error:\n"
                    "            results[device[\"name\"]] = f\"ERROR: {error}\"\n"
                    "    return results\n"
                    "\n"
                    "report = run_on_all(devices, \"show version\", flaky_runner)\n"
                    "for name, result in report.items():\n"
                    "    print(f\"{name}: {result}\")"
                ),
            },
        },

        # ── Lesson 3 ─────────────────────────────────────────────────────────
        {
            "id": "ad-l3-orchestration",
            "title": "Orchestration — Coordinating Many Tasks",
            "duration": "20 min",
            "objectives": [
                "Tell automation and orchestration apart",
                "Read a basic Ansible playbook",
                "Build a step runner that rolls back on failure",
            ],
            "sections": [
                {
                    "heading": "Automation vs Orchestration",
                    "body": (
                        "Automation does one task automatically (push a config). "
                        "Orchestration coordinates many automated tasks together, "
                        "in order, often across systems: provision a VLAN -> "
                        "update the firewall rule -> update DNS -> notify Slack. "
                        "Ansible playbooks are a common orchestration tool."
                    ),
                    "code": (
                        "---\n"
                        "- name: Configure SNMP on all routers\n"
                        "  hosts: routers\n"
                        "  gather_facts: no\n"
                        "  tasks:\n"
                        "    - name: Set SNMP community\n"
                        "      ios_config:\n"
                        "        lines:\n"
                        "          - snmp-server community MyReadOnlyString RO"
                    ),
                    "note": "Real Ansible YAML syntax -- run with `ansible-playbook snmp-config.yml`, not Python.",
                },
            ],
            "exercise": {
                "title": "Build a Step Runner With Rollback",
                "instruction": (
                    "Write a function run_workflow(steps) where steps is a list "
                    "of (description, function) tuples. Run each step in order. "
                    "If any step raises an exception, print which step failed, "
                    "stop running further steps, and call any '_undo' function "
                    "already attached to completed steps in REVERSE order "
                    "(simple rollback). Track completed steps in a list as you go."
                ),
                "starter_code": (
                    "log = []\n"
                    "\n"
                    "def provision_vlan():\n"
                    "    log.append(\"vlan provisioned\")\n"
                    "\n"
                    "def undo_provision_vlan():\n"
                    "    log.append(\"vlan rolled back\")\n"
                    "\n"
                    "def update_firewall():\n"
                    "    log.append(\"firewall updated\")\n"
                    "\n"
                    "def undo_update_firewall():\n"
                    "    log.append(\"firewall rolled back\")\n"
                    "\n"
                    "def update_dns():\n"
                    "    raise RuntimeError(\"DNS server unreachable\")\n"
                    "\n"
                    "steps = [\n"
                    "    (\"provision vlan\", provision_vlan, undo_provision_vlan),\n"
                    "    (\"update firewall\", update_firewall, undo_update_firewall),\n"
                    "    (\"update dns\", update_dns, None),\n"
                    "]\n"
                    "\n"
                    "def run_workflow(steps):\n"
                    "    completed = []\n"
                    "    for description, action, undo in steps:\n"
                    "        try:\n"
                    "            action()\n"
                    "            completed.append((description, undo))\n"
                    "        except Exception as error:\n"
                    "            print(f\"Step failed: {description} ({error})\")\n"
                    "            print(\"Rolling back completed steps...\")\n"
                    "            for description2, undo2 in reversed(completed):\n"
                    "                if undo2:\n"
                    "                    undo2()\n"
                    "            return False\n"
                    "    return True\n"
                    "\n"
                    "success = run_workflow(steps)\n"
                    "print(\"Workflow succeeded\" if success else \"Workflow failed and rolled back\")\n"
                    "print(\"Log:\", log)"
                ),
            },
        },

        # ── Lesson 4 ─────────────────────────────────────────────────────────
        {
            "id": "ad-l4-dna-center",
            "title": "Cisco DNA Center — One Dashboard, One API",
            "duration": "15 min",
            "objectives": [
                "Name DNA Center's four core workflow areas",
                "Read a basic DNA Center REST API call",
                "Filter a simulated device-list API response",
            ],
            "sections": [
                {
                    "heading": "Design, Policy, Provision, Assurance",
                    "body": (
                        "DNA Center is Cisco's centralized dashboard sitting on "
                        "top of everything in this course: Design defines the "
                        "network hierarchy, Policy defines access rules, "
                        "Provision pushes config (the automation layer), and "
                        "Assurance gives health dashboards and AI-driven issue "
                        "detection. It's also a REST API you can script against."
                    ),
                    "code": (
                        "import requests\n"
                        "\n"
                        "url = \"https://dnac.example.com/dna/intent/api/v1/network-device\"\n"
                        "headers = {\"X-Auth-Token\": \"your-token-here\"}\n"
                        "response = requests.get(url, headers=headers, verify=False)\n"
                        "print(response.json())"
                    ),
                    "note": "Needs the `requests` library and a real DNA Center instance -- won't run in this sandbox. Try Cisco's free DevNet DNA Center Sandbox for the real thing.",
                },
            ],
            "exercise": {
                "title": "Filter a Simulated DNA Center Response",
                "instruction": (
                    "DNA Center's API would hand you back JSON like the "
                    "sample below. Write a function unhealthy_devices(response) "
                    "that returns the names of every device with healthScore "
                    "below 7."
                ),
                "starter_code": (
                    "simulated_response = {\n"
                    "    \"response\": [\n"
                    "        {\"hostname\": \"core-sw1\", \"healthScore\": 10},\n"
                    "        {\"hostname\": \"edge-rtr2\", \"healthScore\": 4},\n"
                    "        {\"hostname\": \"access-sw3\", \"healthScore\": 6},\n"
                    "    ]\n"
                    "}\n"
                    "\n"
                    "def unhealthy_devices(response):\n"
                    "    return [\n"
                    "        device[\"hostname\"]\n"
                    "        for device in response[\"response\"]\n"
                    "        if device[\"healthScore\"] < 7\n"
                    "    ]\n"
                    "\n"
                    "print(\"Needs attention:\", unhealthy_devices(simulated_response))"
                ),
            },
        },

        # ── Lesson 5 ─────────────────────────────────────────────────────────
        {
            "id": "ad-l5-study-strategies",
            "title": "Study Strategies and Exam Tips",
            "duration": "10 min",
            "objectives": [
                "Build a habit of labbing every command instead of just reading it",
                "Use the 'teach it back' test to check real understanding",
                "Build a simple spaced-review tracker",
            ],
            "sections": [
                {
                    "heading": "Five Things That Actually Work",
                    "body": (
                        "Lab everything -- reading commands isn't the same as "
                        "knowing them. Build a command cheat sheet as you go, "
                        "kebab-case file per topic. Teach it back: if you can "
                        "explain ACLs to a friend in plain English, you get it; "
                        "if not, you memorized it. Chunk by 'why' not just 'how' "
                        "-- know why `ip access-group 110 in` uses `in` and not "
                        "`out`. The day before the exam: don't cram new topics, "
                        "redo your cheat sheet from memory and patch the gaps."
                    ),
                    "code": None,
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a Spaced-Review Tracker",
                "instruction": (
                    "Write a function topics_due_for_review(topics, today) that "
                    "takes a list of {'topic': str, 'last_reviewed_day': int} "
                    "dicts and an integer 'today', and returns the names of "
                    "topics where today - last_reviewed_day >= 3 (due for "
                    "another pass)."
                ),
                "starter_code": (
                    "topics = [\n"
                    "    {\"topic\": \"ACLs\", \"last_reviewed_day\": 1},\n"
                    "    {\"topic\": \"SNMP\", \"last_reviewed_day\": 5},\n"
                    "    {\"topic\": \"NetFlow\", \"last_reviewed_day\": 6},\n"
                    "]\n"
                    "today = 8\n"
                    "\n"
                    "def topics_due_for_review(topics, today):\n"
                    "    return [\n"
                    "        t[\"topic\"] for t in topics\n"
                    "        if today - t[\"last_reviewed_day\"] >= 3\n"
                    "    ]\n"
                    "\n"
                    "print(\"Review today:\", topics_due_for_review(topics, today))"
                ),
            },
        },
    ],
}
