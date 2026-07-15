# ─────────────────────────────────────────────────────────────────────────────
# Network Automation chapter — Paramiko · Netmiko · Ansible · NAPALM · Telnet
# Drop this dict into the CHAPTERS list in app/content.py (see header there).
# Matches your existing chapter/lesson structure exactly.
#
# Design note on the "Real Driver" sections: the production-grade code shown
# there is the genuine library code (real imports, real device IPs) — it
# needs `pip install <library>` plus an actual reachable device, so clicking
# "Run in Editor" on it will fail in this sandbox (ModuleNotFoundError, a
# connection error, or a timeout). That failure is expected and is called
# out in each section's `note`. The "Practice Safely" section right after it
# and the lesson's exercise use a small in-script simulated device instead,
# so the exact same class shape (connect → send_command → close) actually
# runs end to end with zero new dependencies and zero real network access.
# ─────────────────────────────────────────────────────────────────────────────

NETWORK_AUTOMATION_CHAPTER = {
    "id": "ch-network-automation",
    "number": 7,
    "title": "Network Automation Drivers",
    "subtitle": "Paramiko · Netmiko · Ansible · NAPALM · Telnet",
    "description": (
        "Five tools, one workflow: Inventory → Connect → Execute → Parse → Act. "
        "Build a driver class for each tool, see the real production code "
        "every tool ships with, then practice the exact same pattern safely "
        "against a simulated device — no lab gear required."
    ),
    "further_reading": [
        {"title": "Network Automation — Baby Steps Guide", "url": "/resource/network-automation-baby-steps-guide"},
        {"title": "Network Automation — Discussion", "url": "/resource/network-automation-discussion"},
        {"title": "Python Network Automation — Pocket Reference", "url": "/resource/python-network-automation-pocket-reference"},
    ],
    "lessons": [

        # ── Lesson 1 ─────────────────────────────────────────────────────────
        {
            "id": "na-l1-paramiko",
            "title": "Paramiko — Your First SSH Driver",
            "duration": "20 min",
            "objectives": [
                "Map an SSH session to connect → send_command → close",
                "Build a minimal Paramiko-style driver class",
                "Practice the pattern safely before touching a real device",
            ],
            "sections": [
                {
                    "heading": "Why Paramiko First",
                    "body": (
                        "Paramiko is the lowest-level tool of the five: it knows SSH, "
                        "and nothing else. It doesn't know it's talking to a Cisco "
                        "router versus a Linux box — you handle every detail yourself. "
                        "That makes it verbose, but it's the best place to start because "
                        "nothing is hidden. Every other tool in this chapter is built on "
                        "the same idea: open a connection, send text, read the reply, "
                        "close the connection."
                    ),
                    "code": None,
                    "note": None,
                },
                {
                    "heading": "The Real Driver (Lab / Real-Device Code)",
                    "body": (
                        "This is the production-grade version — the exact shape you'd "
                        "deploy against a real device in GNS3, EVE-NG, or Cisco CML."
                    ),
                    "code": (
                        "import paramiko\n"
                        "\n"
                        "class paramiko_driver:\n"
                        "    def __init__(self, hostname, username, password):\n"
                        "        self.hostname = hostname\n"
                        "        self.username = username\n"
                        "        self.password = password\n"
                        "        self.client = paramiko.SSHClient()\n"
                        "        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())\n"
                        "\n"
                        "    def connect(self):\n"
                        "        self.client.connect(\n"
                        "            hostname=self.hostname,\n"
                        "            username=self.username,\n"
                        "            password=self.password,\n"
                        "        )\n"
                        "\n"
                        "    def send_command(self, command):\n"
                        "        stdin, stdout, stderr = self.client.exec_command(command)\n"
                        "        return stdout.read().decode('utf-8')\n"
                        "\n"
                        "    def close(self):\n"
                        "        self.client.close()\n"
                        "\n"
                        "ssh = paramiko_driver('192.168.1.10', 'admin', 'secret')\n"
                        "ssh.connect()\n"
                        "print(ssh.send_command('uptime'))\n"
                        "ssh.close()"
                    ),
                    "note": (
                        "Lab-only: needs `pip install paramiko` plus a reachable SSH "
                        "host. Running it here raises ModuleNotFoundError — that's "
                        "expected. Try the simulated version below instead."
                    ),
                },
                {
                    "heading": "Practice Safely — Simulated SSH Session",
                    "body": (
                        "Same class shape, real method names — connect(), send_command(), "
                        "close() — but the transport underneath is a small in-script "
                        "stand-in instead of a real SSH handshake. The muscle memory "
                        "transfers directly to the real paramiko.SSHClient() above."
                    ),
                    "code": (
                        "class simulated_ssh_session:\n"
                        "    \"\"\"Stands in for paramiko.SSHClient -- same connect / send / close shape.\"\"\"\n"
                        "\n"
                        "    _CANNED_REPLIES = {\n"
                        "        'uptime': '14:02:07 up 19 days,  3:41,  1 user,  load average: 0.04, 0.02, 0.01',\n"
                        "        'show version': 'Cisco IOS Software, Version 15.2(7)E3, edge-router-1',\n"
                        "        'whoami': 'admin',\n"
                        "    }\n"
                        "\n"
                        "    def __init__(self, hostname, username, password):\n"
                        "        self.hostname = hostname\n"
                        "        self.username = username\n"
                        "        self.password = password\n"
                        "        self.connected = False\n"
                        "\n"
                        "    def connect(self):\n"
                        "        # A real paramiko.SSHClient() would open a TCP + SSH handshake here.\n"
                        "        self.connected = True\n"
                        "\n"
                        "    def send_command(self, command):\n"
                        "        if not self.connected:\n"
                        "            raise RuntimeError('Call connect() before sending commands.')\n"
                        "        return self._CANNED_REPLIES.get(command, f'% Unknown command: {command}')\n"
                        "\n"
                        "    def close(self):\n"
                        "        self.connected = False\n"
                        "\n"
                        "\n"
                        "class paramiko_style_driver:\n"
                        "    def __init__(self, hostname, username, password):\n"
                        "        self.hostname = hostname\n"
                        "        self.username = username\n"
                        "        self.password = password\n"
                        "        self.session = simulated_ssh_session(hostname, username, password)\n"
                        "\n"
                        "    def connect(self):\n"
                        "        self.session.connect()\n"
                        "\n"
                        "    def send_command(self, command):\n"
                        "        return self.session.send_command(command)\n"
                        "\n"
                        "    def close(self):\n"
                        "        self.session.close()\n"
                        "\n"
                        "\n"
                        "driver = paramiko_style_driver('edge-router-1', 'admin', 'secret')\n"
                        "driver.connect()\n"
                        "print(driver.send_command('uptime'))\n"
                        "print(driver.send_command('show version'))\n"
                        "driver.close()"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Add Convenience Methods to Your Driver",
                "instruction": (
                    "Extend paramiko_style_driver with get_uptime() and get_version() "
                    "convenience methods, then add a status_report() method that "
                    "combines both into one line. Run it to see the combined report."
                ),
                "starter_code": (
                    "class simulated_ssh_session:\n"
                    "    \"\"\"Stands in for paramiko.SSHClient -- same connect / send / close shape.\"\"\"\n"
                    "\n"
                    "    _CANNED_REPLIES = {\n"
                    "        'uptime': '14:02:07 up 19 days,  3:41,  1 user,  load average: 0.04, 0.02, 0.01',\n"
                    "        'show version': 'Cisco IOS Software, Version 15.2(7)E3, edge-router-1',\n"
                    "    }\n"
                    "\n"
                    "    def __init__(self, hostname, username, password):\n"
                    "        self.hostname = hostname\n"
                    "        self.username = username\n"
                    "        self.password = password\n"
                    "        self.connected = False\n"
                    "\n"
                    "    def connect(self):\n"
                    "        self.connected = True\n"
                    "\n"
                    "    def send_command(self, command):\n"
                    "        if not self.connected:\n"
                    "            raise RuntimeError('Call connect() before sending commands.')\n"
                    "        return self._CANNED_REPLIES.get(command, f'% Unknown command: {command}')\n"
                    "\n"
                    "    def close(self):\n"
                    "        self.connected = False\n"
                    "\n"
                    "\n"
                    "class paramiko_style_driver:\n"
                    "    def __init__(self, hostname, username, password):\n"
                    "        self.hostname = hostname\n"
                    "        self.username = username\n"
                    "        self.password = password\n"
                    "        self.session = simulated_ssh_session(hostname, username, password)\n"
                    "\n"
                    "    def connect(self):\n"
                    "        self.session.connect()\n"
                    "\n"
                    "    def send_command(self, command):\n"
                    "        return self.session.send_command(command)\n"
                    "\n"
                    "    def close(self):\n"
                    "        self.session.close()\n"
                    "\n"
                    "    # --- exercise additions ---\n"
                    "    def get_uptime(self):\n"
                    "        return self.send_command('uptime')\n"
                    "\n"
                    "    def get_version(self):\n"
                    "        return self.send_command('show version')\n"
                    "\n"
                    "    def status_report(self):\n"
                    "        return f'{self.hostname} | uptime: {self.get_uptime()} | version: {self.get_version()}'\n"
                    "\n"
                    "\n"
                    "driver = paramiko_style_driver('edge-router-1', 'admin', 'secret')\n"
                    "driver.connect()\n"
                    "print(driver.status_report())\n"
                    "driver.close()"
                ),
            },
        },

        # ── Lesson 2 ─────────────────────────────────────────────────────────
        {
            "id": "na-l2-netmiko",
            "title": "Netmiko — SSH That Knows It's a Router",
            "duration": "20 min",
            "objectives": [
                "Understand the device_type parameter and what it buys you",
                "Use send_command() vs send_config_set()",
                "Decide when to reach for Netmiko instead of raw Paramiko",
            ],
            "sections": [
                {
                    "heading": "Why Netmiko",
                    "body": (
                        "Netmiko is Paramiko with one extra ingredient: device_type. "
                        "Tell it the device is 'cisco_ios' and it automatically handles "
                        "the things Paramiko makes you do by hand — paging through long "
                        "output, entering enable mode, knowing what a config prompt looks "
                        "like. If your target is a router, switch, or firewall, this is "
                        "almost always the better starting point over raw Paramiko."
                    ),
                    "code": None,
                    "note": None,
                },
                {
                    "heading": "The Real Driver (Lab / Real-Device Code)",
                    "body": "The production version, including the device_params dictionary Netmiko expects.",
                    "code": (
                        "from netmiko import ConnectHandler\n"
                        "\n"
                        "class netmiko_driver:\n"
                        "    def __init__(self, device_params):\n"
                        "        self.device_params = device_params\n"
                        "        self.connection = None\n"
                        "\n"
                        "    def connect(self):\n"
                        "        self.connection = ConnectHandler(**self.device_params)\n"
                        "\n"
                        "    def get_version(self):\n"
                        "        return self.connection.send_command('show version')\n"
                        "\n"
                        "    def configure_acl(self, acl_lines):\n"
                        "        return self.connection.send_config_set(acl_lines)\n"
                        "\n"
                        "    def disconnect(self):\n"
                        "        if self.connection:\n"
                        "            self.connection.disconnect()\n"
                        "\n"
                        "ios_device = {\n"
                        "    'device_type': 'cisco_ios',\n"
                        "    'host': '192.168.1.1',\n"
                        "    'username': 'admin',\n"
                        "    'password': 'secret',\n"
                        "}\n"
                        "\n"
                        "net = netmiko_driver(ios_device)\n"
                        "net.connect()\n"
                        "print(net.get_version())\n"
                        "net.disconnect()"
                    ),
                    "note": (
                        "Lab-only: needs `pip install netmiko` plus a reachable device. "
                        "Running it here raises ModuleNotFoundError — expected."
                    ),
                },
                {
                    "heading": "Practice Safely — Simulated Netmiko Session",
                    "body": (
                        "The simulated session takes the same device_params dict a real "
                        "ConnectHandler would, and exposes the same three methods you'd "
                        "actually call: send_command, send_config_set, disconnect."
                    ),
                    "code": (
                        "class simulated_netmiko_session:\n"
                        "    \"\"\"Mimics netmiko.ConnectHandler: knows the device_type up front and\n"
                        "    exposes send_command / send_config_set / disconnect.\"\"\"\n"
                        "\n"
                        "    def __init__(self, device_params):\n"
                        "        self.device_params = device_params\n"
                        "        self.connected = False\n"
                        "        self.applied_config = []\n"
                        "\n"
                        "    def connect(self):\n"
                        "        self.connected = True\n"
                        "\n"
                        "    def send_command(self, command):\n"
                        "        if command == 'show version':\n"
                        "            return f\"{self.device_params['device_type']} -- edge-router-1, uptime 19 days\"\n"
                        "        return f'% Unknown command: {command}'\n"
                        "\n"
                        "    def send_config_set(self, lines):\n"
                        "        self.applied_config.extend(lines)\n"
                        "        return '\\n'.join(f'edge-router-1(config)# {line}' for line in lines)\n"
                        "\n"
                        "    def disconnect(self):\n"
                        "        self.connected = False\n"
                        "\n"
                        "\n"
                        "class netmiko_style_driver:\n"
                        "    def __init__(self, device_params):\n"
                        "        self.device_params = device_params\n"
                        "        self.connection = simulated_netmiko_session(device_params)\n"
                        "\n"
                        "    def connect(self):\n"
                        "        self.connection.connect()\n"
                        "\n"
                        "    def get_version(self):\n"
                        "        return self.connection.send_command('show version')\n"
                        "\n"
                        "    def configure_acl(self, acl_lines):\n"
                        "        return self.connection.send_config_set(acl_lines)\n"
                        "\n"
                        "    def disconnect(self):\n"
                        "        self.connection.disconnect()\n"
                        "\n"
                        "\n"
                        "ios_device = {'device_type': 'cisco_ios', 'host': 'edge-router-1'}\n"
                        "net = netmiko_style_driver(ios_device)\n"
                        "net.connect()\n"
                        "print(net.get_version())\n"
                        "print(net.configure_acl([\n"
                        "    'ip access-list extended BLOCK_BAD',\n"
                        "    'deny ip 10.0.0.0 0.255.255.255 any',\n"
                        "    'permit ip any any',\n"
                        "]))\n"
                        "net.disconnect()"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Add save() to Your Driver",
                "instruction": (
                    "Netmiko's real connection has a save_config() method that writes "
                    "the running config to startup config. Add the same to the simulated "
                    "session and a matching save() method on the driver, then call it "
                    "after applying the ACL."
                ),
                "starter_code": (
                    "class simulated_netmiko_session:\n"
                    "    def __init__(self, device_params):\n"
                    "        self.device_params = device_params\n"
                    "        self.connected = False\n"
                    "        self.applied_config = []\n"
                    "        self.saved = False\n"
                    "\n"
                    "    def connect(self):\n"
                    "        self.connected = True\n"
                    "\n"
                    "    def send_command(self, command):\n"
                    "        if command == 'show version':\n"
                    "            return f\"{self.device_params['device_type']} -- edge-router-1, uptime 19 days\"\n"
                    "        return f'% Unknown command: {command}'\n"
                    "\n"
                    "    def send_config_set(self, lines):\n"
                    "        self.applied_config.extend(lines)\n"
                    "        return '\\n'.join(f'edge-router-1(config)# {line}' for line in lines)\n"
                    "\n"
                    "    def save_config(self):\n"
                    "        self.saved = True\n"
                    "        return 'Building configuration...\\n[OK]'\n"
                    "\n"
                    "    def disconnect(self):\n"
                    "        self.connected = False\n"
                    "\n"
                    "\n"
                    "class netmiko_style_driver:\n"
                    "    def __init__(self, device_params):\n"
                    "        self.device_params = device_params\n"
                    "        self.connection = simulated_netmiko_session(device_params)\n"
                    "\n"
                    "    def connect(self):\n"
                    "        self.connection.connect()\n"
                    "\n"
                    "    def get_version(self):\n"
                    "        return self.connection.send_command('show version')\n"
                    "\n"
                    "    def configure_acl(self, acl_lines):\n"
                    "        return self.connection.send_config_set(acl_lines)\n"
                    "\n"
                    "    # --- exercise addition: mirrors Netmiko's real save_config() ---\n"
                    "    def save(self):\n"
                    "        return self.connection.save_config()\n"
                    "\n"
                    "    def disconnect(self):\n"
                    "        self.connection.disconnect()\n"
                    "\n"
                    "\n"
                    "ios_device = {'device_type': 'cisco_ios', 'host': 'edge-router-1'}\n"
                    "net = netmiko_style_driver(ios_device)\n"
                    "net.connect()\n"
                    "print(net.get_version())\n"
                    "print(net.configure_acl(['ip access-list extended BLOCK_BAD', 'deny ip 10.0.0.0 0.255.255.255 any', 'permit ip any any']))\n"
                    "print(net.save())\n"
                    "net.disconnect()"
                ),
            },
        },

        # ── Lesson 3 ─────────────────────────────────────────────────────────
        {
            "id": "na-l3-ansible",
            "title": "Ansible — Automating a Fleet, Not One Device",
            "duration": "25 min",
            "objectives": [
                "Explain the difference between connecting to one device and describing a fleet-wide end state",
                "Define idempotent and recognize it in running code",
                "Build a fleet runner that applies a rule across many simulated devices",
            ],
            "sections": [
                {
                    "heading": "Why Ansible — Thinking in Fleets",
                    "body": (
                        "Paramiko and Netmiko connect to one device per script run. "
                        "Ansible flips the approach entirely: instead of scripting steps, "
                        "you describe the end state you want, and it figures out how to "
                        "get every device in the inventory there. The other defining "
                        "feature is idempotency — running the same playbook twice should "
                        "never produce a different result the second time."
                    ),
                    "code": None,
                    "note": None,
                },
                {
                    "heading": "The Real Driver (Lab / Real-Device Code)",
                    "body": (
                        "A real Ansible setup is two files (an inventory and a playbook) "
                        "plus, if you want to trigger it from Python, a thin wrapper "
                        "around ansible_runner."
                    ),
                    "code": (
                        "# inventory.ini\n"
                        "[cisco_routers]\n"
                        "192.168.1.1 ansible_network_os=ios ansible_user=admin ansible_password=secret\n"
                        "\n"
                        "# backup.yml\n"
                        "- name: Backup router configs\n"
                        "  hosts: cisco_routers\n"
                        "  gather_facts: no\n"
                        "  tasks:\n"
                        "    - name: Run show running-config\n"
                        "      ios_command:\n"
                        "        commands: show running-config\n"
                        "      register: config_output\n"
                        "    - name: Save to file\n"
                        "      copy:\n"
                        "        content: \"{{ config_output.stdout[0] }}\"\n"
                        "        dest: \"backups/{{ inventory_hostname }}.cfg\"\n"
                        "\n"
                        "# Driving it from Python:\n"
                        "import ansible_runner\n"
                        "\n"
                        "class ansible_fleet_runner:\n"
                        "    def __init__(self, playbook_path, inventory_path):\n"
                        "        self.playbook_path = playbook_path\n"
                        "        self.inventory_path = inventory_path\n"
                        "\n"
                        "    def run(self):\n"
                        "        result = ansible_runner.run(\n"
                        "            private_data_dir='.',\n"
                        "            playbook=self.playbook_path,\n"
                        "            inventory=self.inventory_path,\n"
                        "        )\n"
                        "        return result.status, result.rc\n"
                        "\n"
                        "runner = ansible_fleet_runner('backup.yml', 'inventory.ini')\n"
                        "print(runner.run())"
                    ),
                    "note": (
                        "Lab-only: the top two blocks are YAML and INI, not Python — "
                        "running this here raises a SyntaxError, which is expected. The "
                        "Python class also needs `pip install ansible-runner` plus real "
                        "playbook/inventory files and reachable devices."
                    ),
                },
                {
                    "heading": "Practice Safely — Simulated Fleet Runner",
                    "body": (
                        "No YAML engine here — just the concept that matters: one rule, "
                        "applied to every device, with each device deciding for itself "
                        "whether a change is even needed. Run this twice in your head and "
                        "notice the second run should report no changes anywhere."
                    ),
                    "code": (
                        "class simulated_fleet_device:\n"
                        "    def __init__(self, name, running_config):\n"
                        "        self.name = name\n"
                        "        self.running_config = running_config\n"
                        "\n"
                        "    def apply_if_missing(self, required_line):\n"
                        "        if required_line in self.running_config:\n"
                        "            return f'{self.name}: already present -- {required_line}'\n"
                        "        self.running_config.append(required_line)\n"
                        "        return f'{self.name}: ADDED -- {required_line}'\n"
                        "\n"
                        "\n"
                        "class fleet_runner:\n"
                        "    \"\"\"Stands in for an Ansible playbook run: the same task, applied\n"
                        "    across every device in the inventory, idempotently.\"\"\"\n"
                        "\n"
                        "    def __init__(self, devices):\n"
                        "        self.devices = devices\n"
                        "\n"
                        "    def run_playbook(self, required_line):\n"
                        "        return [device.apply_if_missing(required_line) for device in self.devices]\n"
                        "\n"
                        "\n"
                        "fleet = [\n"
                        "    simulated_fleet_device('edge-router-1', ['ip ssh version 2']),\n"
                        "    simulated_fleet_device('edge-router-2', ['ip ssh version 2', 'ntp server 10.0.0.1']),\n"
                        "    simulated_fleet_device('core-switch-1', []),\n"
                        "]\n"
                        "\n"
                        "runner = fleet_runner(fleet)\n"
                        "\n"
                        "print('First run:')\n"
                        "for line in runner.run_playbook('ntp server 10.0.0.1'):\n"
                        "    print(' ', line)\n"
                        "\n"
                        "print()\n"
                        "print('Running the exact same playbook again -- nothing should change:')\n"
                        "for line in runner.run_playbook('ntp server 10.0.0.1'):\n"
                        "    print(' ', line)"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Run a Two-Rule Golden-Config Audit",
                "instruction": (
                    "Extend fleet_runner.run_playbook() to accept a list of golden "
                    "rules instead of one line, apply every rule to every device, and "
                    "print a summary: how many changes were made vs how many devices "
                    "were already compliant."
                ),
                "starter_code": (
                    "class simulated_fleet_device:\n"
                    "    def __init__(self, name, running_config):\n"
                    "        self.name = name\n"
                    "        self.running_config = running_config\n"
                    "\n"
                    "    def apply_if_missing(self, required_line):\n"
                    "        if required_line in self.running_config:\n"
                    "            return False, f'{self.name}: already compliant -- {required_line}'\n"
                    "        self.running_config.append(required_line)\n"
                    "        return True, f'{self.name}: ADDED -- {required_line}'\n"
                    "\n"
                    "\n"
                    "class fleet_runner:\n"
                    "    def __init__(self, devices):\n"
                    "        self.devices = devices\n"
                    "\n"
                    "    def run_playbook(self, required_lines):\n"
                    "        changed = 0\n"
                    "        for required_line in required_lines:\n"
                    "            for device in self.devices:\n"
                    "                was_changed, message = device.apply_if_missing(required_line)\n"
                    "                print(' ', message)\n"
                    "                if was_changed:\n"
                    "                    changed += 1\n"
                    "        return changed\n"
                    "\n"
                    "\n"
                    "fleet = [\n"
                    "    simulated_fleet_device('edge-router-1', ['ip ssh version 2']),\n"
                    "    simulated_fleet_device('edge-router-2', ['ip ssh version 2', 'ntp server 10.0.0.1']),\n"
                    "    simulated_fleet_device('core-switch-1', []),\n"
                    "]\n"
                    "\n"
                    "golden_rules = ['ip ssh version 2', 'ntp server 10.0.0.1']\n"
                    "runner = fleet_runner(fleet)\n"
                    "\n"
                    "print(f'Applying {len(golden_rules)} golden-config rules across {len(fleet)} devices:')\n"
                    "total_changes = runner.run_playbook(golden_rules)\n"
                    "\n"
                    "print()\n"
                    "print(f'Summary: {total_changes} change(s) made, '\n"
                    "      f'{len(fleet) * len(golden_rules) - total_changes} already compliant.')"
                ),
            },
        },

        # ── Lesson 4 ─────────────────────────────────────────────────────────
        {
            "id": "na-l4-napalm",
            "title": "NAPALM — One API, Many Vendors",
            "duration": "20 min",
            "objectives": [
                "Explain what 'multivendor abstraction' actually buys you",
                "Use load_merge_candidate() / compare_config() to preview a change before applying it",
                "Decide between commit() and rollback() based on a diff",
            ],
            "sections": [
                {
                    "heading": "Why NAPALM",
                    "body": (
                        "Cisco, Juniper, and Arista each speak their own CLI dialect. "
                        "NAPALM hides those differences behind one shared Python API, so "
                        "the same driver code works no matter the vendor underneath. Its "
                        "standout safety feature is compare_config() — it shows you the "
                        "diff of a proposed change before anything is actually applied."
                    ),
                    "code": None,
                    "note": None,
                },
                {
                    "heading": "The Real Driver (Lab / Real-Device Code)",
                    "body": "Notice the review-before-commit pattern: load, compare, then decide.",
                    "code": (
                        "from napalm import get_network_driver\n"
                        "\n"
                        "class napalm_driver:\n"
                        "    def __init__(self, vendor, hostname, username, password):\n"
                        "        driver = get_network_driver(vendor)\n"
                        "        self.device = driver(hostname, username, password)\n"
                        "\n"
                        "    def connect(self):\n"
                        "        self.device.open()\n"
                        "\n"
                        "    def load_and_merge(self, config_file):\n"
                        "        self.device.load_merge_candidate(filename=config_file)\n"
                        "        return self.device.compare_config()\n"
                        "\n"
                        "    def commit(self):\n"
                        "        self.device.commit_config()\n"
                        "\n"
                        "    def rollback(self):\n"
                        "        self.device.discard_config()\n"
                        "\n"
                        "    def disconnect(self):\n"
                        "        self.device.close()\n"
                        "\n"
                        "napalm = napalm_driver('ios', '192.168.1.1', 'admin', 'secret')\n"
                        "napalm.connect()\n"
                        "diff = napalm.load_and_merge('snippets/ntp.cfg')\n"
                        "print(diff)\n"
                        "if 'ntp server' in diff:\n"
                        "    napalm.commit()\n"
                        "else:\n"
                        "    napalm.rollback()\n"
                        "napalm.disconnect()"
                    ),
                    "note": (
                        "Lab-only: needs `pip install napalm` plus the matching vendor "
                        "driver and a reachable device. Running it here raises "
                        "ModuleNotFoundError — expected."
                    ),
                },
                {
                    "heading": "Practice Safely — Simulated Multivendor Diff/Commit",
                    "body": (
                        "The same driver class wraps two completely different simulated "
                        "vendors below. That's the entire point of NAPALM: one class, "
                        "any vendor underneath."
                    ),
                    "code": (
                        "class simulated_napalm_device:\n"
                        "    def __init__(self, vendor, hostname):\n"
                        "        self.vendor = vendor\n"
                        "        self.hostname = hostname\n"
                        "        self._pending_diff = ''\n"
                        "\n"
                        "    def open(self):\n"
                        "        pass\n"
                        "\n"
                        "    def load_merge_candidate(self, config_text):\n"
                        "        self._pending_diff = config_text\n"
                        "\n"
                        "    def compare_config(self):\n"
                        "        return self._pending_diff\n"
                        "\n"
                        "    def commit_config(self):\n"
                        "        result = f'{self.hostname} ({self.vendor}): COMMITTED -> {self._pending_diff.strip()}'\n"
                        "        self._pending_diff = ''\n"
                        "        return result\n"
                        "\n"
                        "    def discard_config(self):\n"
                        "        result = f'{self.hostname} ({self.vendor}): DISCARDED -> {self._pending_diff.strip()}'\n"
                        "        self._pending_diff = ''\n"
                        "        return result\n"
                        "\n"
                        "    def close(self):\n"
                        "        pass\n"
                        "\n"
                        "\n"
                        "class napalm_style_driver:\n"
                        "    def __init__(self, device):\n"
                        "        self.device = device\n"
                        "\n"
                        "    def connect(self):\n"
                        "        self.device.open()\n"
                        "\n"
                        "    def load_and_merge(self, config_text):\n"
                        "        self.device.load_merge_candidate(config_text)\n"
                        "        return self.device.compare_config()\n"
                        "\n"
                        "    def commit(self):\n"
                        "        return self.device.commit_config()\n"
                        "\n"
                        "    def rollback(self):\n"
                        "        return self.device.discard_config()\n"
                        "\n"
                        "    def disconnect(self):\n"
                        "        self.device.close()\n"
                        "\n"
                        "\n"
                        "fleet = [\n"
                        "    napalm_style_driver(simulated_napalm_device('ios', 'edge-router-1')),\n"
                        "    napalm_style_driver(simulated_napalm_device('junos', 'core-switch-1')),\n"
                        "]\n"
                        "\n"
                        "for driver in fleet:\n"
                        "    driver.connect()\n"
                        "    diff = driver.load_and_merge('+ ntp server 10.0.0.1')\n"
                        "    print(diff)\n"
                        "    if 'ntp server' in diff:\n"
                        "        print(driver.commit())\n"
                        "    else:\n"
                        "        print(driver.rollback())\n"
                        "    driver.disconnect()"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Trigger a Real Rollback",
                "instruction": (
                    "Add a third simulated device whose proposed change is unrelated to "
                    "NTP (e.g. an interface description change). Confirm the driver "
                    "correctly rolls it back instead of committing, and print a final "
                    "count of committed vs rolled-back devices."
                ),
                "starter_code": (
                    "class simulated_napalm_device:\n"
                    "    def __init__(self, vendor, hostname):\n"
                    "        self.vendor = vendor\n"
                    "        self.hostname = hostname\n"
                    "        self._pending_diff = ''\n"
                    "\n"
                    "    def open(self):\n"
                    "        pass\n"
                    "\n"
                    "    def load_merge_candidate(self, config_text):\n"
                    "        self._pending_diff = config_text\n"
                    "\n"
                    "    def compare_config(self):\n"
                    "        return self._pending_diff\n"
                    "\n"
                    "    def commit_config(self):\n"
                    "        result = f'{self.hostname} ({self.vendor}): COMMITTED -> {self._pending_diff.strip()}'\n"
                    "        self._pending_diff = ''\n"
                    "        return result\n"
                    "\n"
                    "    def discard_config(self):\n"
                    "        result = f'{self.hostname} ({self.vendor}): DISCARDED -> {self._pending_diff.strip()}'\n"
                    "        self._pending_diff = ''\n"
                    "        return result\n"
                    "\n"
                    "    def close(self):\n"
                    "        pass\n"
                    "\n"
                    "\n"
                    "class napalm_style_driver:\n"
                    "    def __init__(self, device):\n"
                    "        self.device = device\n"
                    "\n"
                    "    def connect(self):\n"
                    "        self.device.open()\n"
                    "\n"
                    "    def load_and_merge(self, config_text):\n"
                    "        self.device.load_merge_candidate(config_text)\n"
                    "        return self.device.compare_config()\n"
                    "\n"
                    "    def commit(self):\n"
                    "        return self.device.commit_config()\n"
                    "\n"
                    "    def rollback(self):\n"
                    "        return self.device.discard_config()\n"
                    "\n"
                    "    def disconnect(self):\n"
                    "        self.device.close()\n"
                    "\n"
                    "\n"
                    "# Three devices, three proposed changes -- only NTP-related ones should commit.\n"
                    "fleet = [\n"
                    "    (napalm_style_driver(simulated_napalm_device('ios', 'edge-router-1')), '+ ntp server 10.0.0.1'),\n"
                    "    (napalm_style_driver(simulated_napalm_device('junos', 'core-switch-1')), '+ ntp server 10.0.0.1'),\n"
                    "    (napalm_style_driver(simulated_napalm_device('eos', 'access-switch-1')), '+ description UNRELATED_CHANGE'),\n"
                    "]\n"
                    "\n"
                    "committed, rolled_back = 0, 0\n"
                    "for driver, proposed_change in fleet:\n"
                    "    driver.connect()\n"
                    "    diff = driver.load_and_merge(proposed_change)\n"
                    "    print(diff)\n"
                    "    if 'ntp server' in diff:\n"
                    "        print(driver.commit())\n"
                    "        committed += 1\n"
                    "    else:\n"
                    "        print(driver.rollback())\n"
                    "        rolled_back += 1\n"
                    "    driver.disconnect()\n"
                    "\n"
                    "print()\n"
                    "print(f'{committed} committed, {rolled_back} rolled back.')"
                ),
            },
        },

        # ── Lesson 5 ─────────────────────────────────────────────────────────
        {
            "id": "na-l5-telnet",
            "title": "Telnet — Why You'll (Almost) Never Use It",
            "duration": "15 min",
            "objectives": [
                "Explain why Telnet credentials are visible to anyone on the wire",
                "Watch plaintext credentials cross a real (local) socket",
                "Know when Telnet is still defensible to use",
            ],
            "sections": [
                {
                    "heading": "Why This Tool Still Exists",
                    "body": (
                        "Telnet does the same job as SSH — open a remote CLI session — "
                        "but it predates encryption being standard. Every password and "
                        "command travels as plain, readable bytes. You'll only reach for "
                        "it against genuinely ancient lab gear with no SSH option, or "
                        "inside a controlled lab/CTF environment where seeing the danger "
                        "first-hand is the point of the exercise."
                    ),
                    "code": None,
                    "note": (
                        "Python's telnetlib has been deprecated since Python 3.11 and is "
                        "slated for removal in 3.13 — the standard library itself is "
                        "moving away from it."
                    ),
                },
                {
                    "heading": "The Real Driver (Lab / Real-Device Code)",
                    "body": "The shape is the same connect / send_command / close pattern as every other driver in this chapter.",
                    "code": (
                        "import telnetlib\n"
                        "import time\n"
                        "\n"
                        "class telnet_driver:\n"
                        "    def __init__(self, hostname, username, password, timeout=5):\n"
                        "        self.hostname = hostname\n"
                        "        self.username = username\n"
                        "        self.password = password\n"
                        "        self.timeout = timeout\n"
                        "        self.tn = None\n"
                        "\n"
                        "    def connect(self):\n"
                        "        self.tn = telnetlib.Telnet(self.hostname, timeout=self.timeout)\n"
                        "        self.tn.read_until(b'Username: ', self.timeout)\n"
                        "        self.tn.write(self.username.encode() + b'\\n')\n"
                        "        self.tn.read_until(b'Password: ', self.timeout)\n"
                        "        self.tn.write(self.password.encode() + b'\\n')\n"
                        "\n"
                        "    def send_command(self, command):\n"
                        "        self.tn.write(command.encode() + b'\\n')\n"
                        "        time.sleep(1)\n"
                        "        return self.tn.read_very_eager().decode('utf-8', errors='ignore')\n"
                        "\n"
                        "    def close(self):\n"
                        "        if self.tn:\n"
                        "            self.tn.close()\n"
                        "\n"
                        "legacy = telnet_driver('192.168.1.99', 'admin', 'secret')\n"
                        "legacy.connect()\n"
                        "print(legacy.send_command('show version'))\n"
                        "legacy.close()"
                    ),
                    "note": (
                        "Lab-only: needs a real reachable legacy device. Running it here "
                        "will hit a connection error or time out after 5 seconds — "
                        "expected, since 192.168.1.99 doesn't exist in this sandbox."
                    ),
                },
                {
                    "heading": "Practice Safely — Watch the Plaintext",
                    "body": (
                        "This one doesn't need a simulated transport — it's a real "
                        "socket connection, just confined to your own machine "
                        "(127.0.0.1) instead of a real switch. A tiny background thread "
                        "plays the part of the legacy device."
                    ),
                    "code": (
                        "import socket\n"
                        "import threading\n"
                        "\n"
                        "def fake_legacy_switch(server_socket, ready_event):\n"
                        "    \"\"\"A toy server that mimics a legacy device's Telnet-style login prompt.\"\"\"\n"
                        "    server_socket.listen(1)\n"
                        "    ready_event.set()\n"
                        "    conn, _ = server_socket.accept()\n"
                        "    conn.sendall(b'Username: ')\n"
                        "    conn.recv(1024)\n"
                        "    conn.sendall(b'Password: ')\n"
                        "    conn.recv(1024)\n"
                        "    conn.sendall(b'switch1> ')\n"
                        "    conn.close()\n"
                        "\n"
                        "server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
                        "server.bind(('127.0.0.1', 0))\n"
                        "host, port = server.getsockname()\n"
                        "\n"
                        "ready = threading.Event()\n"
                        "server_thread = threading.Thread(target=fake_legacy_switch, args=(server, ready))\n"
                        "server_thread.start()\n"
                        "ready.wait(timeout=2)\n"
                        "\n"
                        "client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
                        "client.connect((host, port))\n"
                        "\n"
                        "print('Server:', client.recv(1024).decode())\n"
                        "client.sendall(b'admin\\n')\n"
                        "\n"
                        "print('Server:', client.recv(1024).decode())\n"
                        "client.sendall(b'hunter2\\n')\n"
                        "\n"
                        "print('Server:', client.recv(1024).decode())\n"
                        "client.close()\n"
                        "server_thread.join(timeout=2)\n"
                        "server.close()\n"
                        "\n"
                        "print()\n"
                        "print(\"Notice 'admin' and 'hunter2' traveled as plain, readable bytes.\")\n"
                        "print('Anyone capturing this traffic (Wireshark, a switch port mirror, a')\n"
                        "print('compromised hop) reads the username and password directly.')\n"
                        "print('This is exactly what SSH/Paramiko encrypts -- and Telnet never did.')"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Wrap It in a Driver Class",
                "instruction": (
                    "Rebuild the same demo using a legacy_driver class with connect(), "
                    "send_command(), and close() -- the exact same shape as every other "
                    "driver in this chapter -- so the only thing that changes between "
                    "Telnet and Paramiko is what's happening on the wire underneath."
                ),
                "starter_code": (
                    "import socket\n"
                    "import threading\n"
                    "\n"
                    "def fake_legacy_switch(server_socket, ready_event):\n"
                    "    server_socket.listen(1)\n"
                    "    ready_event.set()\n"
                    "    conn, _ = server_socket.accept()\n"
                    "    conn.sendall(b'Username: ')\n"
                    "    conn.recv(1024)\n"
                    "    conn.sendall(b'Password: ')\n"
                    "    conn.recv(1024)\n"
                    "    conn.sendall(b'show version\\r\\nSwitch1, plaintext-OS 1.0\\r\\nswitch1> ')\n"
                    "    conn.close()\n"
                    "\n"
                    "\n"
                    "class legacy_driver:\n"
                    "    \"\"\"Same connect / send_command / close shape as every other driver\n"
                    "    in this chapter -- the only thing that changed is what's happening\n"
                    "    underneath: nothing is encrypted.\"\"\"\n"
                    "\n"
                    "    def __init__(self, host, port, username, password):\n"
                    "        self.host = host\n"
                    "        self.port = port\n"
                    "        self.username = username\n"
                    "        self.password = password\n"
                    "        self.sock = None\n"
                    "\n"
                    "    def connect(self):\n"
                    "        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
                    "        self.sock.connect((self.host, self.port))\n"
                    "        self.sock.recv(1024)\n"
                    "        self.sock.sendall(self.username.encode() + b'\\n')\n"
                    "        self.sock.recv(1024)\n"
                    "        self.sock.sendall(self.password.encode() + b'\\n')\n"
                    "\n"
                    "    def send_command(self, command):\n"
                    "        # A real legacy switch would echo a prompt; here we just read\n"
                    "        # whatever the simulated device already queued up for us.\n"
                    "        return self.sock.recv(4096).decode()\n"
                    "\n"
                    "    def close(self):\n"
                    "        self.sock.close()\n"
                    "\n"
                    "\n"
                    "server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
                    "server.bind(('127.0.0.1', 0))\n"
                    "host, port = server.getsockname()\n"
                    "\n"
                    "ready = threading.Event()\n"
                    "server_thread = threading.Thread(target=fake_legacy_switch, args=(server, ready))\n"
                    "server_thread.start()\n"
                    "ready.wait(timeout=2)\n"
                    "\n"
                    "legacy = legacy_driver(host, port, 'admin', 'hunter2')\n"
                    "legacy.connect()\n"
                    "print(legacy.send_command('show version'))\n"
                    "legacy.close()\n"
                    "server_thread.join(timeout=2)\n"
                    "server.close()\n"
                    "\n"
                    "print(\"Username 'admin' and password 'hunter2' were both sent as plain\")\n"
                    "print('text over that socket -- swap this for paramiko.SSHClient() and')\n"
                    "print('the exact same credentials would be encrypted end to end.')"
                ),
            },
        },
    ],
}
