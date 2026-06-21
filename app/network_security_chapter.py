# ─────────────────────────────────────────────────────────────────────────────
# Network Security chapter — Securing a Network · Password Policies · ACLs ·
# Securing Wi-Fi
# Drop this dict into the CHAPTERS list in app/content.py (see header there).
# Matches your existing chapter/lesson structure exactly.
# ─────────────────────────────────────────────────────────────────────────────

NETWORK_SECURITY_CHAPTER = {
    "id": "ch-network-security",
    "number": 9,
    "title": "Securing the Network",
    "subtitle": "Hardening · Password Policies · ACLs · Wi-Fi Security",
    "description": (
        "Defense in depth, four pieces at a time. Each lesson shows the real "
        "Cisco IOS hardening commands, then a small Python exercise that "
        "practices the same security logic on simulated data."
    ),
    "lessons": [

        # ── Lesson 1 ─────────────────────────────────────────────────────────
        {
            "id": "ns-l1-securing-networks",
            "title": "Securing a Network — Defense in Depth",
            "duration": "15 min",
            "objectives": [
                "Name the core moves of basic network hardening",
                "Disable Telnet in favor of SSH",
                "Build a config hardening checker",
            ],
            "sections": [
                {
                    "heading": "Layered Defense",
                    "body": (
                        "No single control stops every attack, so you stack them: "
                        "disable unused ports/services, use AAA, encrypt "
                        "management traffic (SSH not Telnet), patch regularly, "
                        "and segment with VLANs. If one layer fails, the next one "
                        "catches it."
                    ),
                    "code": (
                        "line vty 0 4\n"
                        " transport input ssh\n"
                        " login local"
                    ),
                    "note": "Real Cisco IOS syntax -- forces SSH-only remote management.",
                },
                {
                    "heading": "Practice — Hardening Checklist",
                    "body": "Same idea as a Python checker over a config dict.",
                    "code": (
                        "config = {\"telnet_enabled\": True, \"unused_ports_disabled\": False}\n"
                        "\n"
                        "if config[\"telnet_enabled\"]:\n"
                        "    print(\"WARNING: Telnet is enabled -- switch to SSH\")\n"
                        "if not config[\"unused_ports_disabled\"]:\n"
                        "    print(\"WARNING: unused ports are still active\")"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a Hardening Auditor",
                "instruction": (
                    "Write a function audit_hardening(config) that checks a "
                    "device config dict for: telnet_enabled (True = bad), "
                    "aaa_enabled (False = bad), unused_ports_disabled (False = "
                    "bad), and patch_level (anything other than 'current' = "
                    "bad). Return a list of warning strings, empty list if clean."
                ),
                "starter_code": (
                    "devices = [\n"
                    "    {\"name\": \"core-sw1\", \"telnet_enabled\": True, \"aaa_enabled\": True,\n"
                    "     \"unused_ports_disabled\": False, \"patch_level\": \"current\"},\n"
                    "    {\"name\": \"edge-rtr2\", \"telnet_enabled\": False, \"aaa_enabled\": False,\n"
                    "     \"unused_ports_disabled\": True, \"patch_level\": \"outdated\"},\n"
                    "]\n"
                    "\n"
                    "def audit_hardening(config):\n"
                    "    warnings = []\n"
                    "    if config.get(\"telnet_enabled\"):\n"
                    "        warnings.append(\"Telnet enabled -- switch to SSH\")\n"
                    "    if not config.get(\"aaa_enabled\"):\n"
                    "        warnings.append(\"AAA not enabled\")\n"
                    "    if not config.get(\"unused_ports_disabled\"):\n"
                    "        warnings.append(\"Unused ports not disabled\")\n"
                    "    if config.get(\"patch_level\") != \"current\":\n"
                    "        warnings.append(\"Device is not on the current patch level\")\n"
                    "    return warnings\n"
                    "\n"
                    "for device in devices:\n"
                    "    print(device[\"name\"], \"->\", audit_hardening(device) or \"clean\")"
                ),
            },
        },

        # ── Lesson 2 ─────────────────────────────────────────────────────────
        {
            "id": "ns-l2-password-policies",
            "title": "Password Policies",
            "duration": "15 min",
            "objectives": [
                "Know why enable secret beats enable password",
                "Configure a minimum length + lockout policy",
                "Build a password policy validator",
            ],
            "sections": [
                {
                    "heading": "Secret vs Password",
                    "body": (
                        "enable secret hashes the password (much stronger); the "
                        "old enable password is reversible -- never use it. Add a "
                        "minimum length and a lockout rule so brute-forcing "
                        "becomes impractical."
                    ),
                    "code": (
                        "service password-encryption\n"
                        "enable secret MyStrongPass!2026\n"
                        "\n"
                        "security passwords min-length 10\n"
                        "login block-for 120 attempts 3 within 60"
                    ),
                    "note": "Real Cisco IOS syntax -- reference only.",
                },
                {
                    "heading": "Practice — Policy Validator",
                    "body": "Checking a password against length + complexity rules in Python.",
                    "code": (
                        "def meets_policy(password, min_length=10):\n"
                        "    has_upper = any(c.isupper() for c in password)\n"
                        "    has_digit = any(c.isdigit() for c in password)\n"
                        "    return len(password) >= min_length and has_upper and has_digit\n"
                        "\n"
                        "print(meets_policy(\"shortpw\"))\n"
                        "print(meets_policy(\"MyStrongPass2026\"))"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a Full Policy Checker",
                "instruction": (
                    "Extend meets_policy into check_password(password) that "
                    "returns a list of every rule it FAILS (empty list = pass). "
                    "Rules: at least 10 characters, at least one uppercase "
                    "letter, at least one digit, at least one symbol from "
                    "'!@#$%^&*', and must not be in a small COMMON_PASSWORDS set."
                ),
                "starter_code": (
                    "COMMON_PASSWORDS = {\"password123\", \"admin123\", \"changeme\"}\n"
                    "candidates = [\"shortpw\", \"password123\", \"MyStrongPass!2026\", \"alllowercase1!\"]\n"
                    "\n"
                    "def check_password(password):\n"
                    "    failures = []\n"
                    "    if len(password) < 10:\n"
                    "        failures.append(\"too short (need 10+ characters)\")\n"
                    "    if not any(c.isupper() for c in password):\n"
                    "        failures.append(\"missing an uppercase letter\")\n"
                    "    if not any(c.isdigit() for c in password):\n"
                    "        failures.append(\"missing a digit\")\n"
                    "    if not any(c in \"!@#$%^&*\" for c in password):\n"
                    "        failures.append(\"missing a symbol\")\n"
                    "    if password.lower() in COMMON_PASSWORDS:\n"
                    "        failures.append(\"is a known common password\")\n"
                    "    return failures\n"
                    "\n"
                    "for pw in candidates:\n"
                    "    result = check_password(pw)\n"
                    "    print(pw, \"->\", result if result else \"PASS\")"
                ),
            },
        },

        # ── Lesson 3 ─────────────────────────────────────────────────────────
        {
            "id": "ns-l3-acls",
            "title": "ACLs — The Network Bouncer",
            "duration": "20 min",
            "objectives": [
                "Tell standard ACLs apart from extended ACLs",
                "Remember the implicit deny-all at the end of every ACL",
                "Build a simple rule-based packet matcher",
            ],
            "sections": [
                {
                    "heading": "Standard vs Extended",
                    "body": (
                        "Standard ACLs filter on source IP only. Extended ACLs "
                        "filter on source, destination, protocol, and port -- "
                        "much more precise. Every ACL has an invisible 'deny any' "
                        "at the very end, so anything you didn't explicitly "
                        "permit gets dropped."
                    ),
                    "code": (
                        "! Extended ACL: only allow 192.168.1.0/24 to reach HTTPS\n"
                        "access-list 110 permit tcp 192.168.1.0 0.0.0.255 any eq 443\n"
                        "access-list 110 deny ip any any\n"
                        "\n"
                        "interface GigabitEthernet0/0\n"
                        " ip access-group 110 in"
                    ),
                    "note": "Real Cisco IOS syntax -- reference only.",
                },
                {
                    "heading": "Practice — Rule Matcher",
                    "body": "The same permit/deny logic as an ordered list of rule dicts checked in Python.",
                    "code": (
                        "rules = [\n"
                        "    {\"action\": \"permit\", \"src\": \"192.168.1.0/24\", \"port\": 443},\n"
                        "    {\"action\": \"deny\", \"src\": \"any\", \"port\": \"any\"},\n"
                        "]\n"
                        "\n"
                        "def check(src, port):\n"
                        "    for rule in rules:\n"
                        "        if rule[\"src\"] in (src, \"any\") and rule[\"port\"] in (port, \"any\"):\n"
                        "            return rule[\"action\"]\n"
                        "    return \"deny\"  # implicit deny-all\n"
                        "\n"
                        "print(check(\"192.168.1.0/24\", 443))\n"
                        "print(check(\"10.0.0.5\", 22))"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build an ACL Simulator",
                "instruction": (
                    "Write a function evaluate_acl(rules, packet) where packet is "
                    "a dict with 'src', 'dst', and 'port'. Walk the rules in "
                    "order, returning the first matching rule's action ('permit' "
                    "or 'deny'). A rule field of 'any' matches everything. If no "
                    "rule matches, return 'deny' (the implicit deny-all). Test "
                    "against the sample packets."
                ),
                "starter_code": (
                    "rules = [\n"
                    "    {\"action\": \"permit\", \"src\": \"192.168.1.0/24\", \"dst\": \"any\", \"port\": 443},\n"
                    "    {\"action\": \"permit\", \"src\": \"192.168.1.0/24\", \"dst\": \"any\", \"port\": 22},\n"
                    "    {\"action\": \"deny\", \"src\": \"any\", \"dst\": \"any\", \"port\": \"any\"},\n"
                    "]\n"
                    "\n"
                    "packets = [\n"
                    "    {\"src\": \"192.168.1.0/24\", \"dst\": \"8.8.8.8\", \"port\": 443},\n"
                    "    {\"src\": \"10.0.0.5\", \"dst\": \"8.8.8.8\", \"port\": 443},\n"
                    "    {\"src\": \"192.168.1.0/24\", \"dst\": \"8.8.8.8\", \"port\": 80},\n"
                    "]\n"
                    "\n"
                    "def evaluate_acl(rules, packet):\n"
                    "    for rule in rules:\n"
                    "        src_match = rule[\"src\"] in (packet[\"src\"], \"any\")\n"
                    "        dst_match = rule[\"dst\"] in (packet[\"dst\"], \"any\")\n"
                    "        port_match = rule[\"port\"] in (packet[\"port\"], \"any\")\n"
                    "        if src_match and dst_match and port_match:\n"
                    "            return rule[\"action\"]\n"
                    "    return \"deny\"\n"
                    "\n"
                    "for packet in packets:\n"
                    "    print(packet, \"->\", evaluate_acl(rules, packet))"
                ),
            },
        },

        # ── Lesson 4 ─────────────────────────────────────────────────────────
        {
            "id": "ns-l4-securing-wifi",
            "title": "Securing Wi-Fi",
            "duration": "15 min",
            "objectives": [
                "Rank WEP, WPA2, and WPA3 by security strength",
                "Know why WPS should be disabled",
                "Build a Wi-Fi config validator",
            ],
            "sections": [
                {
                    "heading": "What Actually Matters",
                    "body": (
                        "Use WPA3 (or WPA2-AES at minimum) -- never WEP or "
                        "WPA-TKIP, both are broken. Disable WPS, it's trivially "
                        "brute-forced. Separate guest and internal SSIDs. For "
                        "enterprise networks, use 802.1X + RADIUS instead of one "
                        "shared passphrase everyone knows."
                    ),
                    "code": (
                        "wlan SecureCorp 1 SecureCorp\n"
                        " security wpa wpa2 ciphers aes\n"
                        " security wpa akm 802.1x\n"
                        " radius_server auth add 1 192.168.1.50 1812 ascii MyRadiusSecret"
                    ),
                    "note": "Conceptual Cisco WLC-style syntax -- reference only.",
                },
                {
                    "heading": "Practice — Quick Validator",
                    "body": "Same logic as a Python check over an AP config dict.",
                    "code": (
                        "ap = {\"security\": \"WPA2-AES\", \"wps_enabled\": True}\n"
                        "\n"
                        "if ap[\"security\"] in (\"WEP\", \"WPA-TKIP\"):\n"
                        "    print(\"CRITICAL: weak encryption in use\")\n"
                        "if ap[\"wps_enabled\"]:\n"
                        "    print(\"WARNING: WPS should be disabled\")"
                    ),
                    "note": None,
                },
            ],
            "exercise": {
                "title": "Build a Wi-Fi Security Scorer",
                "instruction": (
                    "Write a function score_ap(ap) that starts at 100 points and "
                    "deducts: 100 points if security is 'WEP', 50 points if "
                    "security is 'WPA-TKIP', 20 points if wps_enabled is True, "
                    "and 10 points if guest_isolated is False. Return the final "
                    "score (clamped to 0 minimum) plus a verdict: 'secure' (80+), "
                    "'needs improvement' (40-79), or 'critical' (under 40)."
                ),
                "starter_code": (
                    "access_points = [\n"
                    "    {\"name\": \"corp-main\", \"security\": \"WPA3\", \"wps_enabled\": False, \"guest_isolated\": True},\n"
                    "    {\"name\": \"old-ap-lobby\", \"security\": \"WEP\", \"wps_enabled\": True, \"guest_isolated\": False},\n"
                    "    {\"name\": \"guest-net\", \"security\": \"WPA2-AES\", \"wps_enabled\": True, \"guest_isolated\": True},\n"
                    "]\n"
                    "\n"
                    "def score_ap(ap):\n"
                    "    score = 100\n"
                    "    if ap[\"security\"] == \"WEP\":\n"
                    "        score -= 100\n"
                    "    elif ap[\"security\"] == \"WPA-TKIP\":\n"
                    "        score -= 50\n"
                    "    if ap.get(\"wps_enabled\"):\n"
                    "        score -= 20\n"
                    "    if not ap.get(\"guest_isolated\", True):\n"
                    "        score -= 10\n"
                    "    score = max(score, 0)\n"
                    "    if score >= 80:\n"
                    "        verdict = \"secure\"\n"
                    "    elif score >= 40:\n"
                    "        verdict = \"needs improvement\"\n"
                    "    else:\n"
                    "        verdict = \"critical\"\n"
                    "    return score, verdict\n"
                    "\n"
                    "for ap in access_points:\n"
                    "    score, verdict = score_ap(ap)\n"
                    "    print(f\"{ap['name']}: {score}/100 -> {verdict}\")"
                ),
            },
        },
    ],
}
