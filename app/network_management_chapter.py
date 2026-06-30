NETWORK_MANAGEMENT_CHAPTER = {
    "id": "ch-network-management",
    "number": 11,
    "title": "Network Management",
    "subtitle": "FCAPS · SNMP · NetFlow · IP SLA · ACLs · Hardening",
    "description": (
        "From the five FCAPS buckets that define what network management means, "
        "through the monitoring protocols that give you visibility (SNMP, NetFlow, IP SLA), "
        "to the hardening techniques that keep the network secure — then tie it all "
        "together by parsing structured device data with Python."
    ),
    "lessons": [

        # ── Lesson 1 ─────────────────────────────────────────────────────────
        {
            "id": "nm-l1-fcaps",
            "title": "FCAPS — The Five Buckets of Network Management",
            "duration": "20 min",
            "objectives": [
                "Name and describe each FCAPS bucket with a concrete example",
                "Map a real-world network event to the correct bucket",
                "Build a simulated device-state object and classify actions against it",
            ],
            "sections": [
                {
                    "heading": "What Network Management Actually Means",
                    "body": (
                        "Network management is the ongoing work of keeping network devices "
                        "(routers, switches, firewalls, access points) up, fast, correctly "
                        "configured, and secure. That's a broad mandate, so the industry "
                        "organized it into five categories called FCAPS — each one a "
                        "distinct type of work with its own tools and metrics.\n\n"
                        "FCAPS stands for: Fault, Configuration, Accounting, "
                        "Performance, and Security."
                    ),
                    "code": None,
                    "note": None,
                },
                {
                    "heading": "The Five Buckets",
                    "body": (
                        "Fault — detect and fix problems. A switch port flapping up/down, "
                        "a link going dark, a device going offline. Tools: syslog, SNMP "
                        "traps, netflow anomaly detection.\n\n"
                        "Configuration — keep device settings correct and consistent. "
                        "Pushing the same NTP server to 200 routers. Tools: Ansible, "
                        "NAPALM, Netmiko.\n\n"
                        "Accounting — track who used the network, how much, and when. "
                        "Bandwidth billing, department usage reports, audit trails. "
                        "Tools: NetFlow, IPFIX, RADIUS accounting.\n\n"
                        "Performance — keep it fast. Measure latency, packet loss, "
                        "throughput, and intervene before users notice degradation. "
                        "Tools: IP SLA, MRTG, Grafana.\n\n"
                        "Security — keep it safe. ACLs, AAA, encrypted management "
                        "traffic, patch management, anomaly detection. Tools: "
                        "IDS/IPS, ACLs, 802.1X."
                    ),
                    "code": (
                        "fcaps = {\n"
                        "    'fault':         'detect/fix outages and failures',\n"
                        "    'configuration': 'keep device settings correct',\n"
                        "    'accounting':    'track usage and audit trails',\n"
                        "    'performance':   'measure and maintain speed/quality',\n"
                        "    'security':      'protect against unauthorized access',\n"
                        "}\n"
                        "\n"
                        "events = [\n"
                        "    ('Switch port Gi0/1 flapping',          'fault'),\n"
                        "    ('Pushing NTP server to 50 routers',    'configuration'),\n"
                        "    ('Latency to DC spiked from 2ms to 80ms', 'performance'),\n"
                        "    ('Dept A used 40GB this month',         'accounting'),\n"
                        "    ('Brute-force login attempt detected',  'security'),\n"
                        "]\n"
                        "\n"
                        "for event, bucket in events:\n"
                        "    print(f'{bucket.upper():14} | {event}')"
                    ),
                    "note": None,
                },
                {
                    "heading": "The 5-Step Automation Workflow",
                    "body": (
                        "Across every tool in network automation, the same five steps "
                        "repeat: Inventory (know your devices), Connect (SSH/API), "
                        "Execute (send commands), Parse (turn text into data), Act "
                        "(make a decision — save, alert, rollback, or push a change)."
                    ),
                    "code": (
                        "class network_device:\n"
                        "    def __init__(self, hostname, ip, role, running_config):\n"
                        "        self.hostname = hostname\n"
                        "        self.ip = ip\n"
                        "        self.role = role\n"
                        "        self.running_config = running_config\n"
                        "\n"
                        "    def has_line(self, config_line):\n"
                        "        return config_line in self.running_config\n"
                        "\n"
                        "\n"
                        "# Step 1 — Inventory\n"
                        "inventory = [\n"
                        "    network_device('edge-router-1', '192.168.1.1', 'router',\n"
                        "                   ['ip ssh version 2', 'ntp server 10.0.0.1']),\n"
                        "    network_device('core-switch-1', '192.168.1.2', 'switch',\n"
                        "                   ['ip ssh version 2']),\n"
                        "    network_device('access-switch-1', '192.168.1.3', 'switch',\n"
                        "                   []),\n"
                        "]\n"
                        "\n"
                        "required = 'ntp server 10.0.0.1'\n"
                        "\n"
                        "for device in inventory:\n"
                        "    # Step 2: Connect (simulated — real code would use Netmiko here)\n"
                        "    # Step 3: Execute (has_line simulates 'show run | include ntp')\n"
                        "    found = device.has_line(required)\n"
                        "    # Step 4: Parse (bool result)\n"
                        "    status = 'OK' if found else 'MISSING'\n"
                        "    # Step 5: Act\n"
                        "    print(f'{device.hostname:20} {device.ip:15} {status}')"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "FCAPS Classifier",
                "instruction": (
                    "Extend the network_device class with an fcaps_audit() method that "
                    "checks for three config lines (one per FCAPS category: ntp for "
                    "configuration, ip ssh for security, logging for fault) and returns "
                    "a dict mapping each category to 'PASS' or 'FAIL'. Run it against "
                    "the three devices in the inventory."
                ),
                "starter_code": (
                    "class network_device:\n"
                    "    def __init__(self, hostname, ip, running_config):\n"
                    "        self.hostname = hostname\n"
                    "        self.ip = ip\n"
                    "        self.running_config = running_config\n"
                    "\n"
                    "    def has_line(self, line):\n"
                    "        return line in self.running_config\n"
                    "\n"
                    "    def fcaps_audit(self):\n"
                    "        return {\n"
                    "            'configuration': 'PASS' if self.has_line('ntp server 10.0.0.1') else 'FAIL',\n"
                    "            'security':      'PASS' if self.has_line('ip ssh version 2') else 'FAIL',\n"
                    "            'fault':         'PASS' if self.has_line('logging host 10.0.0.5') else 'FAIL',\n"
                    "        }\n"
                    "\n"
                    "\n"
                    "inventory = [\n"
                    "    network_device('edge-router-1', '192.168.1.1',\n"
                    "                   ['ip ssh version 2', 'ntp server 10.0.0.1', 'logging host 10.0.0.5']),\n"
                    "    network_device('core-switch-1', '192.168.1.2',\n"
                    "                   ['ip ssh version 2']),\n"
                    "    network_device('access-switch-1', '192.168.1.3',\n"
                    "                   []),\n"
                    "]\n"
                    "\n"
                    "for device in inventory:\n"
                    "    results = device.fcaps_audit()\n"
                    "    print(f'\\n{device.hostname} ({device.ip})')\n"
                    "    for category, status in results.items():\n"
                    "        print(f'  {category:14} {status}')"
                ),
            },
        },

        # ── Lesson 2 ─────────────────────────────────────────────────────────
        {
            "id": "nm-l2-monitoring",
            "title": "Monitoring — SNMP, NetFlow & IP SLA",
            "duration": "25 min",
            "objectives": [
                "Explain the security difference between SNMPv2c and SNMPv3",
                "Describe what NetFlow records and why it matters for blue-team work",
                "Use IP SLA to catch performance degradation before users notice",
            ],
            "sections": [
                {
                    "heading": "SNMP — Polling Your Devices",
                    "body": (
                        "SNMP (Simple Network Management Protocol) lets a central server "
                        "(Zabbix, PRTG, SolarWinds) poll devices for metrics: CPU load, "
                        "interface traffic, memory use. The server sends a GET request "
                        "and the device replies with the value.\n\n"
                        "SNMPv2c is easy to configure but sends everything in plain text "
                        "— including the community string that acts as a password. Anyone "
                        "on the wire can read it.\n\n"
                        "SNMPv3 adds authentication (SHA) and encryption (AES). More "
                        "steps to configure, but the only acceptable choice on a real network."
                    ),
                    "code": (
                        "# Real Cisco IOS config — requires a router, not runnable here\n"
                        "snmpv2c_config = '''\n"
                        "snmp-server community MyReadOnlyString RO\n"
                        "snmp-server location server-room-1\n"
                        "snmp-server contact admin@example.com\n"
                        "'''\n"
                        "\n"
                        "snmpv3_config = '''\n"
                        "snmp-server group ADMINGROUP v3 priv\n"
                        "snmp-server user netadmin ADMINGROUP v3\n"
                        "  auth sha MyAuthPass123\n"
                        "  priv aes 128 MyPrivPass123\n"
                        "'''\n"
                        "\n"
                        "print('SNMPv2c config lines:')\n"
                        "print(snmpv2c_config)\n"
                        "print('SNMPv3 config lines (auth + encryption):')\n"
                        "print(snmpv3_config)"
                    ),
                    "note": (
                        "The config blocks above are Cisco IOS syntax — they can't run "
                        "in Python directly. Displaying them as strings lets you read "
                        "and study the exact commands."
                    ),
                },
                {
                    "heading": "NetFlow — Who Talked to Who",
                    "body": (
                        "NetFlow records traffic metadata: source IP, destination IP, "
                        "port, protocol, bytes, duration — but not the packet content. "
                        "Think of it like a phone bill: you see who called who and for "
                        "how long, not what was said.\n\n"
                        "For blue-team work, NetFlow is gold. Anomalous traffic "
                        "(a workstation suddenly sending data to an unknown external IP "
                        "at 3am) shows up immediately in NetFlow records even if the "
                        "session is encrypted."
                    ),
                    "code": (
                        "# Practice: Simulate NetFlow record analysis\n"
                        "\n"
                        "flow_records = [\n"
                        "    {'src': '192.168.1.10', 'dst': '8.8.8.8',     'port': 443,  'bytes': 1200,   'hour': 9},\n"
                        "    {'src': '192.168.1.10', 'dst': '8.8.8.8',     'port': 443,  'bytes': 3400,   'hour': 10},\n"
                        "    {'src': '192.168.1.22', 'dst': '45.33.32.156','port': 4444, 'bytes': 980000, 'hour': 3},\n"
                        "    {'src': '192.168.1.15', 'dst': '10.0.0.1',    'port': 22,   'bytes': 512,    'hour': 14},\n"
                        "]\n"
                        "\n"
                        "SUSPICIOUS_PORTS = {4444, 1337, 31337}\n"
                        "OFF_HOURS = range(0, 6)\n"
                        "\n"
                        "print('NetFlow anomaly scan:')\n"
                        "for flow in flow_records:\n"
                        "    flags = []\n"
                        "    if flow['port'] in SUSPICIOUS_PORTS:\n"
                        "        flags.append(f\"suspicious port {flow['port']}\")\n"
                        "    if flow['hour'] in OFF_HOURS and flow['bytes'] > 100000:\n"
                        "        flags.append(f\"large off-hours transfer ({flow['bytes']} bytes)\")\n"
                        "    if flags:\n"
                        "        print(f\"  ALERT {flow['src']} -> {flow['dst']}: {', '.join(flags)}\")\n"
                        "    else:\n"
                        "        print(f\"  OK    {flow['src']} -> {flow['dst']}\")"
                    ),
                    "note": None,
                },
                {
                    "heading": "IP SLA — Proactive Latency Testing",
                    "body": (
                        "IP SLA (Service Level Agreement) tells the router to run "
                        "synthetic tests on a schedule — like an automated ping every "
                        "30 seconds — and log the results. Instead of users calling to "
                        "say 'the internet is slow', the router tells you first.\n\n"
                        "This is Performance management (the P in FCAPS) in practice: "
                        "you define a baseline, set thresholds, and get alerted when "
                        "measured values drift past them."
                    ),
                    "code": (
                        "# Practice: Simulated IP SLA latency monitor\n"
                        "\n"
                        "class ip_sla_monitor:\n"
                        "    def __init__(self, target, threshold_ms):\n"
                        "        self.target = target\n"
                        "        self.threshold_ms = threshold_ms\n"
                        "        self.readings = []\n"
                        "\n"
                        "    def record(self, latency_ms):\n"
                        "        self.readings.append(latency_ms)\n"
                        "        if latency_ms > self.threshold_ms:\n"
                        "            return f'ALERT  {self.target}: latency {latency_ms}ms exceeds threshold {self.threshold_ms}ms'\n"
                        "        return f'OK     {self.target}: latency {latency_ms}ms'\n"
                        "\n"
                        "    def average(self):\n"
                        "        return sum(self.readings) / len(self.readings) if self.readings else 0\n"
                        "\n"
                        "\n"
                        "sla = ip_sla_monitor('data-center-gateway', threshold_ms=50)\n"
                        "\n"
                        "# Simulated readings arriving every 30 seconds\n"
                        "simulated_readings = [2, 3, 4, 2, 78, 92, 85, 3, 2]\n"
                        "for reading in simulated_readings:\n"
                        "    print(sla.record(reading))\n"
                        "\n"
                        "print(f'\\nAverage latency: {sla.average():.1f}ms')"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a Multi-Target SLA Dashboard",
                "instruction": (
                    "Extend ip_sla_monitor so it tracks a violation_count alongside "
                    "the readings list. Then create a dashboard() function that takes "
                    "a list of monitors and prints a summary table: target, readings "
                    "count, average latency, violations, and status (OK if 0 violations, "
                    "DEGRADED if any)."
                ),
                "starter_code": (
                    "class ip_sla_monitor:\n"
                    "    def __init__(self, target, threshold_ms):\n"
                    "        self.target = target\n"
                    "        self.threshold_ms = threshold_ms\n"
                    "        self.readings = []\n"
                    "        self.violation_count = 0\n"
                    "\n"
                    "    def record(self, latency_ms):\n"
                    "        self.readings.append(latency_ms)\n"
                    "        if latency_ms > self.threshold_ms:\n"
                    "            self.violation_count += 1\n"
                    "\n"
                    "    def average(self):\n"
                    "        return sum(self.readings) / len(self.readings) if self.readings else 0\n"
                    "\n"
                    "\n"
                    "def dashboard(monitors):\n"
                    "    print(f'{'Target':<22} {'Readings':>8} {'Avg ms':>7} {'Violations':>11} Status')\n"
                    "    print('-' * 62)\n"
                    "    for m in monitors:\n"
                    "        status = 'OK' if m.violation_count == 0 else 'DEGRADED'\n"
                    "        print(f'{m.target:<22} {len(m.readings):>8} {m.average():>7.1f} {m.violation_count:>11} {status}')\n"
                    "\n"
                    "\n"
                    "targets = [\n"
                    "    ('data-center-gw', 50,  [2, 3, 78, 2, 92, 2]),\n"
                    "    ('branch-office-1', 100, [30, 45, 40, 38]),\n"
                    "    ('cloud-api-east',  80,  [20, 22, 21, 110, 95]),\n"
                    "]\n"
                    "\n"
                    "monitors = []\n"
                    "for name, threshold, readings in targets:\n"
                    "    m = ip_sla_monitor(name, threshold)\n"
                    "    for r in readings:\n"
                    "        m.record(r)\n"
                    "    monitors.append(m)\n"
                    "\n"
                    "dashboard(monitors)"
                ),
            },
        },

        # ── Lesson 3 ─────────────────────────────────────────────────────────
        {
            "id": "nm-l3-hardening",
            "title": "Network Security Hardening",
            "duration": "25 min",
            "objectives": [
                "Apply password policy commands that survive a config audit",
                "Write and test an ACL rule — standard vs extended",
                "Identify the minimum WiFi security standard and why WEP/TKIP fail",
            ],
            "sections": [
                {
                    "heading": "Password Policies on Cisco IOS",
                    "body": (
                        "There are two critical differences most beginners miss:\n\n"
                        "1. enable secret vs enable password — secret uses MD5+ hashing; "
                        "password is reversible with a simple Cisco tool. Always use secret.\n\n"
                        "2. service password-encryption only encrypts type-7 (weak, reversible). "
                        "It hides passwords from shoulder-surfing, not from a real attacker. "
                        "Pair it with proper secret commands, never rely on it alone.\n\n"
                        "login block-for is the key lockout command — it rate-limits failed "
                        "attempts before a brute-force can get anywhere."
                    ),
                    "code": (
                        "password_policy_config = '''\n"
                        "service password-encryption\n"
                        "enable secret MyStrongPass!2026\n"
                        "\n"
                        "username admin privilege 15 secret AnotherStrong!2026\n"
                        "\n"
                        "security passwords min-length 10\n"
                        "login block-for 120 attempts 3 within 60\n"
                        "\n"
                        "line vty 0 4\n"
                        " transport input ssh\n"
                        " login local\n"
                        "'''\n"
                        "\n"
                        "print('Password hardening config:')\n"
                        "for line in password_policy_config.strip().splitlines():\n"
                        "    print(f'  {line}')"
                    ),
                    "note": (
                        "This is Cisco IOS syntax shown as a Python string — "
                        "study the commands, then practice them in Packet Tracer."
                    ),
                },
                {
                    "heading": "ACLs — The Network Bouncer",
                    "body": (
                        "Access Control Lists filter traffic on a router interface. "
                        "Standard ACLs match on source IP only — blunt but fast. "
                        "Extended ACLs match on source, destination, port, and protocol "
                        "— more precise, preferred in real deployments.\n\n"
                        "The most important rule: every ACL ends with an implicit "
                        "deny any. If you don't explicitly permit traffic, it gets "
                        "dropped silently. Always check hit counts with show access-lists."
                    ),
                    "code": (
                        "# Practice: Python ACL rule engine (same logic as IOS ACL matching)\n"
                        "\n"
                        "class acl_rule:\n"
                        "    def __init__(self, action, src_network, src_mask, dst_port=None):\n"
                        "        self.action = action\n"
                        "        self.src_prefix = src_network.rsplit('.', 1)[0]\n"
                        "        self.dst_port = dst_port\n"
                        "\n"
                        "    def matches(self, src_ip, dst_port=None):\n"
                        "        src_match = src_ip.startswith(self.src_prefix)\n"
                        "        port_match = (self.dst_port is None) or (dst_port == self.dst_port)\n"
                        "        return src_match and port_match\n"
                        "\n"
                        "\n"
                        "class access_list:\n"
                        "    def __init__(self, name):\n"
                        "        self.name = name\n"
                        "        self.rules = []\n"
                        "        self.hit_counts = []\n"
                        "\n"
                        "    def add_rule(self, action, src_network, src_mask, dst_port=None):\n"
                        "        self.rules.append(acl_rule(action, src_network, src_mask, dst_port))\n"
                        "        self.hit_counts.append(0)\n"
                        "\n"
                        "    def check(self, src_ip, dst_port=None):\n"
                        "        for i, rule in enumerate(self.rules):\n"
                        "            if rule.matches(src_ip, dst_port):\n"
                        "                self.hit_counts[i] += 1\n"
                        "                return rule.action\n"
                        "        return 'deny'\n"
                        "\n"
                        "\n"
                        "# Extended ACL: only 192.168.1.x can reach port 443, block everything else\n"
                        "acl110 = access_list('BLOCK_EXTERNAL')\n"
                        "acl110.add_rule('permit', '192.168.1.0', '0.0.0.255', dst_port=443)\n"
                        "acl110.add_rule('deny',   '0.0.0.0',     '255.255.255.255')\n"
                        "\n"
                        "test_traffic = [\n"
                        "    ('192.168.1.55', 443),\n"
                        "    ('192.168.1.55', 80),\n"
                        "    ('10.0.0.99',    443),\n"
                        "    ('172.16.0.1',   22),\n"
                        "]\n"
                        "\n"
                        "for src, port in test_traffic:\n"
                        "    result = acl110.check(src, port)\n"
                        "    print(f'{result.upper():6} {src}:{port}')"
                    ),
                    "note": None,
                },
                {
                    "heading": "WiFi Security Standards",
                    "body": (
                        "WEP — broken. Cracked in minutes with aircrack-ng. Never use it.\n"
                        "WPA-TKIP — deprecated. Shares WEP's RC4 cipher, still vulnerable.\n"
                        "WPA2-AES — minimum acceptable. Strong encryption, widely supported.\n"
                        "WPA3 — current standard. Protects against offline dictionary attacks "
                        "with SAE (Simultaneous Authentication of Equals).\n\n"
                        "WPS (Wi-Fi Protected Setup) looks convenient but its 8-digit PIN "
                        "can be brute-forced in hours. Disable it.\n\n"
                        "For enterprise: 802.1X + RADIUS server instead of a shared "
                        "passphrase. Each user authenticates individually — one compromised "
                        "password doesn't hand over the whole network."
                    ),
                    "code": (
                        "wifi_standards = {\n"
                        "    'WEP':       {'status': 'BROKEN',     'note': 'cracked in minutes — never use'},\n"
                        "    'WPA-TKIP':  {'status': 'DEPRECATED', 'note': 'shares WEP vulnerabilities'},\n"
                        "    'WPA2-AES':  {'status': 'ACCEPTABLE', 'note': 'minimum for production'},\n"
                        "    'WPA3-SAE':  {'status': 'RECOMMENDED','note': 'current standard, offline attack resistant'},\n"
                        "    '802.1X':    {'status': 'ENTERPRISE',  'note': 'per-user auth via RADIUS'},\n"
                        "}\n"
                        "\n"
                        "for standard, info in wifi_standards.items():\n"
                        "    print(f'{standard:10} [{info[\"status\"]:11}] {info[\"note\"]}')"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Hardening Audit — ACL + Policy Check",
                "instruction": (
                    "Build a hardening_auditor class that takes a device's running_config "
                    "list and checks: (1) 'enable secret' present, (2) 'transport input ssh' "
                    "present, (3) 'login block-for' present, (4) 'service password-encryption' "
                    "present. Run it against three devices and print PASS/FAIL per check."
                ),
                "starter_code": (
                    "class hardening_auditor:\n"
                    "    CHECKS = [\n"
                    "        ('enable secret',          'security',      'no enable secret — password reversible'),\n"
                    "        ('transport input ssh',     'security',      'Telnet may be allowed on VTY lines'),\n"
                    "        ('login block-for',         'security',      'no login lockout — brute-force risk'),\n"
                    "        ('service password-encryption', 'configuration', 'passwords visible in running-config'),\n"
                    "    ]\n"
                    "\n"
                    "    def __init__(self, hostname, running_config):\n"
                    "        self.hostname = hostname\n"
                    "        self.running_config = running_config\n"
                    "\n"
                    "    def audit(self):\n"
                    "        print(f'\\n{self.hostname}')\n"
                    "        for check, category, failure_msg in self.CHECKS:\n"
                    "            passed = any(check in line for line in self.running_config)\n"
                    "            status = 'PASS' if passed else 'FAIL'\n"
                    "            note = '' if passed else f'  <- {failure_msg}'\n"
                    "            print(f'  [{status}] {check}{note}')\n"
                    "\n"
                    "\n"
                    "devices = [\n"
                    "    ('edge-router-1', [\n"
                    "        'enable secret MyStrongPass!2026',\n"
                    "        'service password-encryption',\n"
                    "        'transport input ssh',\n"
                    "        'login block-for 120 attempts 3 within 60',\n"
                    "    ]),\n"
                    "    ('core-switch-1', [\n"
                    "        'enable secret WeakPass',\n"
                    "        'transport input ssh',\n"
                    "    ]),\n"
                    "    ('access-switch-1', []),\n"
                    "]\n"
                    "\n"
                    "for hostname, config in devices:\n"
                    "    hardening_auditor(hostname, config).audit()"
                ),
            },
        },

        # ── Lesson 4 ─────────────────────────────────────────────────────────
        {
            "id": "nm-l4-python-data",
            "title": "Python for Network Data — JSON, XML & Idempotent Pushes",
            "duration": "25 min",
            "objectives": [
                "Parse JSON and XML device data with Python's standard library",
                "Implement the idempotent check-before-push pattern in Python",
                "Explain why a script that runs twice should change nothing on the second run",
            ],
            "sections": [
                {
                    "heading": "JSON — The Language of Modern Network APIs",
                    "body": (
                        "Modern network APIs (Cisco DNA Center, Meraki, AWS) return JSON. "
                        "It's the same format your browser uses for AJAX — lightweight, "
                        "human-readable, and trivially parseable in Python with json.loads().\n\n"
                        "Rule of thumb: if the API is less than 10 years old, it speaks JSON. "
                        "If it's a legacy system (NETCONF, SOAP, older Cisco), it speaks XML."
                    ),
                    "code": (
                        "import json\n"
                        "\n"
                        "# Simulated API response from a network device\n"
                        "raw_json = '''{\n"
                        "  \"hostname\": \"edge-router-1\",\n"
                        "  \"interfaces\": [\n"
                        "    {\"name\": \"GigabitEthernet0/0\", \"status\": \"up\",   \"ip\": \"192.168.1.1\"},\n"
                        "    {\"name\": \"GigabitEthernet0/1\", \"status\": \"down\", \"ip\": \"10.0.0.1\"},\n"
                        "    {\"name\": \"Loopback0\",          \"status\": \"up\",   \"ip\": \"1.1.1.1\"}\n"
                        "  ]\n"
                        "}'''\n"
                        "\n"
                        "data = json.loads(raw_json)\n"
                        "\n"
                        "print(f\"Device: {data['hostname']}\")\n"
                        "print('Interface status:')\n"
                        "for iface in data['interfaces']:\n"
                        "    flag = '  UP' if iface['status'] == 'up' else 'DOWN'\n"
                        "    print(f\"  [{flag}] {iface['name']:28} {iface['ip']}\")"
                    ),
                    "note": None,
                },
                {
                    "heading": "XML — Legacy Protocol Data (NETCONF / SOAP)",
                    "body": (
                        "NETCONF — the network configuration protocol used by many "
                        "enterprise devices — uses XML. Python's built-in "
                        "xml.etree.ElementTree handles it without any pip install."
                    ),
                    "code": (
                        "import xml.etree.ElementTree as ET\n"
                        "\n"
                        "xml_data = '''<device>\n"
                        "  <hostname>core-switch-1</hostname>\n"
                        "  <interface name=\"Gi0/0\">up</interface>\n"
                        "  <interface name=\"Gi0/1\">down</interface>\n"
                        "  <interface name=\"Gi0/2\">up</interface>\n"
                        "</device>'''\n"
                        "\n"
                        "root = ET.fromstring(xml_data)\n"
                        "\n"
                        "print(f\"Device: {root.find('hostname').text}\")\n"
                        "print('Interfaces:')\n"
                        "for iface in root.findall('interface'):\n"
                        "    status = iface.text\n"
                        "    flag = '  UP' if status == 'up' else 'DOWN'\n"
                        "    print(f\"  [{flag}] {iface.attrib['name']}\")"
                    ),
                    "note": None,
                },
                {
                    "heading": "Idempotent Config Push — Look Before You Leap",
                    "body": (
                        "The single most important pattern in network automation: "
                        "check whether a change is needed before making it. A script "
                        "that runs the same change twice without checking creates "
                        "duplicate config lines — and on Cisco IOS some duplicate lines "
                        "stack silently, causing subtle misbehavior.\n\n"
                        "The check-before-push pattern (from the discussion notes) is "
                        "idempotency in practice: run it once, run it ten times — the "
                        "network ends up in the same state either way."
                    ),
                    "code": (
                        "class simulated_device_connection:\n"
                        "    \"\"\"Simulates a Netmiko ConnectHandler for safe sandbox practice.\"\"\"\n"
                        "\n"
                        "    def __init__(self, hostname, running_config):\n"
                        "        self.hostname = hostname\n"
                        "        self._config = list(running_config)\n"
                        "        self._changes = []\n"
                        "\n"
                        "    def send_command(self, cmd):\n"
                        "        if 'include' in cmd:\n"
                        "            keyword = cmd.split('include')[-1].strip()\n"
                        "            return '\\n'.join(line for line in self._config if keyword in line)\n"
                        "        return '\\n'.join(self._config)\n"
                        "\n"
                        "    def send_config_set(self, lines):\n"
                        "        for line in lines:\n"
                        "            if line not in self._config:\n"
                        "                self._config.append(line)\n"
                        "                self._changes.append(line)\n"
                        "        return f'{self.hostname}: applied {len(lines)} line(s)'\n"
                        "\n"
                        "    def disconnect(self):\n"
                        "        pass\n"
                        "\n"
                        "\n"
                        "def idempotent_push(conn, config_line):\n"
                        "    current = conn.send_command(f'show run | include {config_line}')\n"
                        "    if config_line in current:\n"
                        "        return f'{conn.hostname}: already present — skipping'\n"
                        "    conn.send_config_set([config_line])\n"
                        "    return f'{conn.hostname}: ADDED {config_line}'\n"
                        "\n"
                        "\n"
                        "devices = [\n"
                        "    simulated_device_connection('edge-router-1', ['ip ssh version 2', 'ntp server 10.0.0.1']),\n"
                        "    simulated_device_connection('core-switch-1', ['ip ssh version 2']),\n"
                        "    simulated_device_connection('access-switch-1', []),\n"
                        "]\n"
                        "\n"
                        "print('First run:')\n"
                        "for dev in devices:\n"
                        "    print(' ', idempotent_push(dev, 'ntp server 10.0.0.1'))\n"
                        "\n"
                        "print('\\nSecond run (nothing should change):')\n"
                        "for dev in devices:\n"
                        "    print(' ', idempotent_push(dev, 'ntp server 10.0.0.1'))"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Parse a JSON Inventory and Flag Down Interfaces",
                "instruction": (
                    "Parse the JSON string below — it contains three devices, each with "
                    "a list of interfaces. Write a function audit_interfaces(json_str) "
                    "that returns a list of (hostname, interface_name) tuples for every "
                    "interface whose status is 'down'. Print the results."
                ),
                "starter_code": (
                    "import json\n"
                    "\n"
                    "inventory_json = '''[\n"
                    "  {\"hostname\": \"edge-router-1\", \"interfaces\": [\n"
                    "    {\"name\": \"Gi0/0\", \"status\": \"up\"},\n"
                    "    {\"name\": \"Gi0/1\", \"status\": \"down\"}\n"
                    "  ]},\n"
                    "  {\"hostname\": \"core-switch-1\", \"interfaces\": [\n"
                    "    {\"name\": \"Gi0/0\", \"status\": \"up\"},\n"
                    "    {\"name\": \"Gi0/1\", \"status\": \"up\"},\n"
                    "    {\"name\": \"Gi0/2\", \"status\": \"down\"}\n"
                    "  ]},\n"
                    "  {\"hostname\": \"access-switch-1\", \"interfaces\": [\n"
                    "    {\"name\": \"Fa0/1\", \"status\": \"down\"},\n"
                    "    {\"name\": \"Fa0/2\", \"status\": \"up\"}\n"
                    "  ]}\n"
                    "]'''\n"
                    "\n"
                    "\n"
                    "def audit_interfaces(json_str):\n"
                    "    devices = json.loads(json_str)\n"
                    "    down = []\n"
                    "    for device in devices:\n"
                    "        for iface in device['interfaces']:\n"
                    "            if iface['status'] == 'down':\n"
                    "                down.append((device['hostname'], iface['name']))\n"
                    "    return down\n"
                    "\n"
                    "\n"
                    "results = audit_interfaces(inventory_json)\n"
                    "print(f'{len(results)} down interface(s) found:')\n"
                    "for hostname, iface in results:\n"
                    "    print(f'  {hostname}: {iface} is DOWN')"
                ),
            },
        },
    ],
}
