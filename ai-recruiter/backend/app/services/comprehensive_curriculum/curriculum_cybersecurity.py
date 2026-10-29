"""
curriculum_cybersecurity.py - Complete 8 Chapters Comprehensive Curriculum for Cybersecurity.
Every chapter contains:
1. Detailed Concepts & In-Depth Explanation
2. Key Formulas, Rules & Architecture
3. Step-by-Step Solved Examples with working code and breakdown
4. Practice Questions with Answers & Explanations
5. Company Placement Technical Interview Questions & Answers
"""
from typing import List, Dict, Any

CYBERSECURITY_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Cybersecurity Foundations, CIA Triad & Threat Modeling",
        "key_takeaways": "Master Confidentiality, Integrity, Availability, STRIDE threat modeling, and defense-in-depth principles.",
        "topics": [
            "The CIA Triad and the Parkerian Hexad security attributes",
            "Threat actors, attack vectors, and MITRE ATT&CK framework matrix",
            "STRIDE Threat Modeling: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege",
            "Defense-in-Depth layered architecture across host, network, app & data",
            "Security standards and compliance frameworks: NIST CSF, ISO 27001 & CIS Benchmarks"
        ],
        "sections": {
            "concept": "Cybersecurity is the discipline of protecting digital assets, networks, devices, and data from unauthorized access, compromise, or destruction. The core paradigm rests upon the CIA Triad: Confidentiality (data is hidden from unauthorized entities), Integrity (data remains unaltered and trustworthy), and Availability (systems and data are accessible to authorized users when needed). The STRIDE model, developed by Microsoft, categorizes software threats systematically during architectural design. Defense-in-depth implements redundant defensive controls at every layer (perimeter firewall, network segmentation, host endpoint detection, application input validation, and data encryption) so that a failure at one tier is contained.",
            "formulas": "1. Risk Formula: Risk = Threat x Vulnerability x Asset_Impact\n2. DREAD Scoring: Score = (Damage + Reproducibility + Exploitability + Affected_Users + Discoverability) / 5\n3. Single Loss Expectancy (SLE): SLE = Asset_Value x Exposure_Factor",
            "solved_examples": [
                {
                    "title": "Applying STRIDE Threat Modeling to an E-Commerce API",
                    "difficulty": "Medium | Cisco, Palo Alto Networks, Microsoft",
                    "problem": "Identify vulnerabilities and mitigations across the 6 STRIDE categories for a REST payment endpoint.",
                    "step_by_step": [
                        "Step 1: Spoofing: Attacker pretends to be another user. Mitigation: Mutual TLS and signed JWT authentication.",
                        "Step 2: Tampering: Attacker changes payment amount in transit. Mitigation: HMAC-SHA256 message signing and HTTPS TLS 1.3.",
                        "Step 3: Repudiation: User denies placing an order. Mitigation: Cryptographic audit logging with digital signatures.",
                        "Step 4: Information Disclosure: Credit card numbers leaked. Mitigation: AES-256 encryption at rest and tokenization.",
                        "Step 5: Denial of Service: Flood of orders exhausts database. Mitigation: WAF rate limiting and token bucket throttling.",
                        "Step 6: Elevation of Privilege: Normal user calls admin refunds. Mitigation: Role-Based Access Control (RBAC) with least privilege."
                    ],
                    "code_or_math": "# STRIDE Threat Matrix Verification\nSTRIDE = ['Spoofing', 'Tampering', 'Repudiation', 'InfoDisclosure', 'DoS', 'ElevationOfPrivilege']\nfor threat in STRIDE:\n    print(f'Threat: {threat:20} -> Control Implemented: YES')"
                }
            ],
            "practice_questions": [
                {
                    "question": "Which component of the CIA Triad is compromised when ransomware encrypts all production hospital databases, demanding Bitcoin to release the key?",
                    "options": [
                        "Confidentiality only",
                        "Availability",
                        "Non-repudiation",
                        "Federated Authentication"
                    ],
                    "answer": "Availability",
                    "explanation": "Ransomware primarily compromises Availability by preventing legitimate authorized users from accessing critical operational systems and data, even if the data was not exfiltrated."
                }
            ],
            "interview_questions": [
                {
                    "company": "Palo Alto Networks & Microsoft",
                    "question": "What is the difference between a Vulnerability, a Threat, and an Exploit in cybersecurity?",
                    "model_answer": "A Vulnerability is a flaw, bug, or misconfiguration in software or hardware (e.g. an unpatched buffer overflow). A Threat is any potential actor or event capable of causing harm by targeting that weakness (e.g. a cybercrime syndicate). An Exploit is the concrete piece of software, script, or technique engineered by an attacker to weaponize the vulnerability.",
                    "interviewer_tip": "Use the equation: Risk = Threat x Vulnerability x Impact to structure your explanation."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Network Security, Firewalls, IDS/IPS & Packet Analysis (Wireshark)",
        "key_takeaways": "Master TCP/IP 3-way handshake security, stateful packet inspection firewalls, Snort IDS rule syntax, and Wireshark PCAP forensic analysis.",
        "topics": [
            "TCP/IP network layer vulnerabilities: ARP spoofing, IP spoofing, TCP SYN floods & DNS amplification",
            "Firewalls: Packet filtering (L3), Stateful inspection (L4), Next-Generation Firewalls (NGFW / L7 Deep Packet Inspection)",
            "Intrusion Detection Systems (IDS) vs Intrusion Prevention Systems (IPS): Signature vs Anomaly-based detection",
            "Wireshark packet capture analysis: TCP flags (SYN, ACK, FIN, RST), stream reassembly & TLS handshakes",
            "Virtual Private Networks (VPN): IPsec (IKEv2, ESP, AH) in Tunnel vs Transport mode"
        ],
        "sections": {
            "concept": "Network security defends data traveling across private and public communication channels. Attackers exploit vulnerabilities in foundational networking protocols, such as flooding SYN packets to exhaust server connection queues (SYN Flood) or poisoning ARP caches on local subnets. Firewalls govern network perimeters: legacy packet filters examine headers statelessly; stateful firewalls track TCP connection states (NEW, ESTABLISHED, RELATED); Next-Gen Firewalls (NGFW) perform Deep Packet Inspection (DPI) to identify application protocols and decode malware in real time. Wireshark is the standard packet capture analyzer used for forensic traffic inspection.",
            "formulas": "1. TCP 3-Way Handshake: SYN (Seq=x) -> SYN-ACK (Seq=y, Ack=x+1) -> ACK (Seq=x+1, Ack=y+1)\n2. SYN Flood Defense: Backlog Queue Depth and TCP SYN Cookies (hash-based Seq numbers)\n3. Bandwidth Amplification Factor (DNS/NTP): BAF = Amplified_Response_Bytes / Request_Bytes (often 50x to 100x)",
            "solved_examples": [
                {
                    "title": "Analyzing a TCP SYN Flood Attack in Wireshark and Writing Snort IDS Detection Rule",
                    "difficulty": "Hard | Cisco, Mandiant, CrowdStrike",
                    "problem": "Write a Snort IDS rule that alerts when more than 100 inbound TCP SYN packets are received from an external IP within 2 seconds.",
                    "step_by_step": [
                        "Step 1: Set action to `alert` on protocol `tcp` from `$EXTERNAL_NET any` to `$HOME_NET 80`.",
                        "Step 2: Inspect TCP flags: look for `flags:S;` (SYN set without ACK).",
                        "Step 3: Add flow tracking: `flow:to_server;`.",
                        "Step 4: Configure threshold detection: `detection_filter: track by_src, count 100, seconds 2;`.",
                        "Step 5: Add classification and unique SID."
                    ],
                    "code_or_math": "# Snort IDS Rule for SYN Flood Detection\nalert tcp $EXTERNAL_NET any -> $HOME_NET 80 (\n  msg: 'POSSIBLE TCP SYN FLOOD DETECTED';\n  flags: S;\n  flow: to_server;\n  detection_filter: track by_src, count 100, seconds 2;\n  classtype: attempted-dos;\n  sid: 1000001;\n  rev: 1;\n)"
                }
            ],
            "practice_questions": [
                {
                    "question": "How do TCP SYN Cookies protect web servers against TCP SYN flood denial-of-service attacks?",
                    "options": [
                        "By blocking all TCP traffic globally",
                        "By encoding connection state into the initial SYN-ACK sequence number, avoiding allocating memory until the client's final ACK is received",
                        "By requiring all users to solve a Google reCAPTCHA in their terminal",
                        "By disconnecting the server's Ethernet cable"
                    ],
                    "answer": "By encoding connection state into the initial SYN-ACK sequence number, avoiding allocating memory until the client's final ACK is received",
                    "explanation": "SYN Cookies encode client IP, port, and timestamp into a cryptographic hash embedded in the Initial Sequence Number (ISN) of the SYN-ACK. The server allocates zero memory buffer until the client returns a valid ACK containing that sequence number, rendering memory-exhaustion SYN floods harmless."
                }
            ],
            "interview_questions": [
                {
                    "company": "Cisco & Cloudflare",
                    "question": "What is the difference between an Intrusion Detection System (IDS) and an Intrusion Prevention System (IPS)?",
                    "model_answer": "An IDS is deployed out-of-band via a network TAP or SPAN port. It passively monitors traffic and sends alerts on suspicious activity, without adding network latency and without the ability to block packets directly. An IPS is deployed inline directly in the network traffic path. It actively inspects packets in real time and can drop malicious traffic, reset TCP connections, and update firewall rules immediately to halt attacks.",
                    "interviewer_tip": "Contrast out-of-band (promiscuous mode) vs inline deployment modes."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Applied Cryptography, Public Key Infrastructure (PKI) & TLS 1.3",
        "key_takeaways": "Master symmetric vs asymmetric ciphers (AES vs RSA/ECC), cryptographic hashing, digital signatures, PKI certificate chains, and TLS 1.3 handshake.",
        "topics": [
            "Symmetric ciphers: AES-GCM (Authenticated Encryption), ChaCha20-Poly1305, block cipher modes (CBC vs GCM)",
            "Asymmetric encryption & Key Exchange: RSA, Diffie-Hellman (DH), Elliptic Curve Cryptography (ECC / ECDHE)",
            "Cryptographic Hash Functions: SHA-256, SHA-3, HMAC for data integrity & collision resistance",
            "Public Key Infrastructure (PKI): X.509 Certificates, Certificate Authorities (CA), CRLs, OCSP Stapling & Certificate Transparency",
            "Transport Layer Security (TLS 1.3): 1-RTT handshake, Perfect Forward Secrecy (PFS) & zero-RTT resumption"
        ],
        "sections": {
            "concept": "Cryptography is the mathematical foundation of digital security. Symmetric cryptography uses a single shared secret key for high-speed encryption (AES-256 in Galois/Counter Mode provides both confidentiality and data authenticity). Asymmetric cryptography uses a public/private key pair (RSA or Elliptic Curves like Ed25519) for key exchange and digital signatures. A digital signature encrypts a SHA-256 message hash with the sender's private key, guaranteeing authenticity and non-repudiation. Transport Layer Security (TLS 1.3) mandates Ephemeral Diffie-Hellman (ECDHE) for Perfect Forward Secrecy (PFS), guaranteeing that compromising a server's long-term private key in the future cannot decrypt past recorded sessions.",
            "formulas": "1. RSA Encryption / Decryption: C = M^e mod n, M = C^d mod n\n2. HMAC Construction: HMAC(K, m) = H((K xor opad) || H((K xor ipad) || m))\n3. ECC Key Length Equivalence: 256-bit ECC provides equivalent security to 3072-bit RSA with 90% less computational overhead",
            "solved_examples": [
                {
                    "title": "Implementing AES-256-GCM Authenticated Encryption with Integrity Verification in Python",
                    "difficulty": "Medium | Google, Apple, Microsoft",
                    "problem": "Write a secure Python script that encrypts confidential customer records using AES-GCM with a random nonce and authenticates associated metadata.",
                    "step_by_step": [
                        "Step 1: Generate a cryptographically secure 256-bit key using `os.urandom(32)`.",
                        "Step 2: Generate a unique 96-bit Initialization Vector (nonce) for every encryption operation.",
                        "Step 3: Instantiate AES-GCM cipher and pass associated authenticated data (AAD).",
                        "Step 4: Encrypt plaintext and generate a 128-bit authentication tag.",
                        "Step 5: Verify that tampering with a single bit of ciphertext causes decryption to throw an InvalidTag error."
                    ],
                    "code_or_math": "from cryptography.hazmat.primitives.ciphers.aead import AESGCM\nimport os\n\ndef encrypt_record(key, plaintext, metadata):\n    aesgcm = AESGCM(key)\n    nonce = os.urandom(12)\n    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), metadata.encode())\n    return nonce + ciphertext\n\nkey = AESGCM.generate_key(bit_length=256)\nencrypted = encrypt_record(key, 'Salary: $150,000', 'UserID: 1042')\nprint(f'Encrypted payload length: {len(encrypted)} bytes (Nonce + Ciphertext + Tag)')"
                }
            ],
            "practice_questions": [
                {
                    "question": "What security property ensures that if a server's private SSL key is leaked in the future, attackers still CANNOT decrypt previously intercepted and recorded HTTPS traffic?",
                    "options": [
                        "Symmetric hashing",
                        "Perfect Forward Secrecy (PFS)",
                        "Password salting",
                        "Two-factor authentication"
                    ],
                    "answer": "Perfect Forward Secrecy (PFS)",
                    "explanation": "Perfect Forward Secrecy (PFS), achieved via ephemeral Diffie-Hellman key exchange (DHE/ECDHE), generates a unique temporary session key for every single TLS connection. Even if the server's long-term private certificate key is stolen years later, past sessions cannot be decrypted."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google & Apple",
                    "question": "Why is AES in GCM (Galois/Counter Mode) preferred over AES in CBC (Cipher Block Chaining) in modern TLS?",
                    "model_answer": "AES-CBC provides encryption but lacks built-in integrity verification, leaving it vulnerable to padding oracle attacks (e.g. POODLE, Lucky Thirteen) unless paired strictly with separate HMAC. AES-GCM is an Authenticated Encryption with Associated Data (AEAD) mode that provides simultaneous high-speed encryption and cryptographic authentication in hardware, eliminating padding oracle attacks completely while achieving higher parallel throughput.",
                    "interviewer_tip": "Cite 'Padding Oracle Attacks' and 'AEAD' to demonstrate cryptographic depth."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Web Application Security & OWASP Top 10 Vulnerabilities",
        "key_takeaways": "Master diagnosing and mitigating the OWASP Top 10: SQL Injection, XSS, CSRF, SSRF, Broken Access Control, and Insecure Deserialization.",
        "topics": [
            "OWASP Top 10 Overview: Broken Access Control, Cryptographic Failures, Injection, Insecure Design",
            "SQL Injection (SQLi): In-band, Blind (Boolean/Time-based) & defense via Parameterized Prepared Statements",
            "Cross-Site Scripting (XSS): Stored, Reflected, DOM-based & Content Security Policy (CSP) mitigation",
            "Cross-Site Request Forgery (CSRF) & SameSite Cookie flags (Strict, Lax, None)",
            "Server-Side Request Forgery (SSRF) and metadata cloud exploitation defense"
        ],
        "sections": {
            "concept": "Web applications represent the primary external attack surface for modern enterprises. The OWASP Top 10 catalogs the most critical vulnerabilities. Broken Access Control (users accessing other users' records due to missing IDOR checks) is currently #1. SQL Injection occurs when untrusted user input concatenates into database queries, allowing attackers to bypass authentication or extract entire databases; the only robust mitigation is Parameterized Prepared Statements. Cross-Site Scripting (XSS) injects malicious JavaScript into victim browsers, mitigated via context-aware output encoding and strict Content Security Policies (CSP).",
            "formulas": "1. SQL Injection Vulnerability Condition: SQL_Query = 'SELECT * FROM users WHERE user = ' + raw_input\n2. Secure Parameterized Query: Precompiled_AST != Evaluated(User_Input)\n3. CSP Header Syntax: Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com",
            "solved_examples": [
                {
                    "title": "Remediating a Critical SQL Injection and IDOR Flaw in a Node.js / Python API",
                    "difficulty": "Medium | HackerOne, Bugcrowd, Amazon",
                    "problem": "Given vulnerable code: `cursor.execute(f'SELECT * FROM accounts WHERE id = {account_id}')`, fix it to prevent SQLi and enforce user authorization (IDOR protection).",
                    "step_by_step": [
                        "Step 1: Identify SQLi: String interpolation allows injecting `' OR '1'='1`.",
                        "Step 2: Replace with parameterized query using query placeholders (`%s` or `?`).",
                        "Step 3: Identify IDOR: The API queries by `account_id` without verifying if `account_id` belongs to the authenticated user in the JWT session.",
                        "Step 4: Update query to check both: `SELECT * FROM accounts WHERE id = %s AND user_id = %s`.",
                        "Step 5: Return 404/403 if no matching row is returned."
                    ],
                    "code_or_math": "# Secure Parameterized Implementation\ndef get_user_account(db, account_id, authenticated_user_id):\n    query = 'SELECT balance, acc_number FROM accounts WHERE id = %s AND owner_id = %s'\n    cursor.execute(query, (account_id, authenticated_user_id)) # Parameterized & Authorized\n    return cursor.fetchone()"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the only guaranteed, industry-standard mitigation to completely neutralize SQL Injection vulnerabilities?",
                    "options": [
                        "Filtering out single quotes with regex replace",
                        "Using Parameterized Queries / Prepared Statements with Object-Relational Mappers (ORMs)",
                        "Running the database on port 8080 instead of 5432",
                        "Encoding the entire database in Base64"
                    ],
                    "answer": "Using Parameterized Queries / Prepared Statements with Object-Relational Mappers (ORMs)",
                    "explanation": "Parameterized queries separate SQL query code from user data. The database compiles the SQL abstract syntax tree (AST) first, and user input is treated strictly as literal data parameters, making SQL injection mathematically impossible."
                }
            ],
            "interview_questions": [
                {
                    "company": "Meta & Google",
                    "question": "What is an Insecure Direct Object Reference (IDOR) vulnerability, and how do you prevent it in RESTful APIs?",
                    "model_answer": "IDOR is a Broken Access Control vulnerability where an application exposes a direct database key or identifier (e.g. `/api/v1/invoices/10452`) in a URL or request parameter without validating whether the authenticated user has permission to access that specific record. Prevention requires implementing an authorization check on every request: verifying that the requested resource ID belongs to the tenant or user ID extracted from the authenticated session token.",
                    "interviewer_tip": "Cite the principle: Never trust client-supplied resource IDs without session ownership verification."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Identity & Access Management, OAuth 2.0, OpenID Connect & Zero Trust Architecture",
        "key_takeaways": "Master OAuth 2.0 grant types (Authorization Code with PKCE), OIDC JWT claims, Multi-Factor Authentication (MFA), and Zero Trust principles.",
        "topics": [
            "Authentication (AuthN) vs Authorization (AuthZ) in distributed systems",
            "OAuth 2.0 Framework: Roles (Resource Owner, Client, Authorization Server, Resource Server)",
            "OAuth 2.0 Flows: Authorization Code Grant with Proof Key for Code Exchange (PKCE) vs Client Credentials",
            "JSON Web Tokens (JWT): Structure (Header, Payload, Signature), verification, and token revocation strategies",
            "Zero Trust Architecture (ZTA): 'Never Trust, Always Verify', micro-segmentation, and context-aware access"
        ],
        "sections": {
            "concept": "Authentication verifies identity ('Who are you?'); Authorization determines permissions ('What are you allowed to do?'). OAuth 2.0 is the open industry authorization framework that enables third-party applications to obtain limited access to an HTTP service without sharing user credentials. OpenID Connect (OIDC) adds an identity layer on top of OAuth 2.0, issuing an ID Token (JWT) alongside the Access Token. The Authorization Code Flow with PKCE (Proof Key for Code Exchange) protects mobile and Single-Page Applications against authorization code interception. Zero Trust Architecture discards the outdated castle-and-moat perimeter model, demanding continuous authentication and dynamic authorization for every single request.",
            "formulas": "1. JWT Structure: base64Url(Header) + '.' + base64Url(Payload) + '.' + Signature\n2. PKCE Verification: code_challenge = base64Url(SHA-256(code_verifier))\n3. Zero Trust Access Decision: Decision = f(User_Identity, Device_Health, GeoLocation, Time, Resource_Sensitivity)",
            "solved_examples": [
                {
                    "title": "Verifying a Cryptographically Signed JWT Token in API Middleware",
                    "difficulty": "Medium | Okta, Auth0, Microsoft",
                    "problem": "Write a secure JWT verification function in Python that checks signature validity, expiration time, and required issuer.",
                    "step_by_step": [
                        "Step 1: Extract Bearer token from HTTP Authorization header.",
                        "Step 2: Decode token using the authorization server's public RSA/ECDSA key.",
                        "Step 3: Verify standard claims: `exp` (expiration timestamp), `iss` (valid issuer), `aud` (expected audience).",
                        "Step 4: Check token blacklist in Redis for revoked session IDs.",
                        "Step 5: Attach verified user payload to the request context."
                    ],
                    "code_or_math": "import jwt\n\ndef verify_jwt_token(token, public_key):\n    try:\n        payload = jwt.decode(\n            token, public_key, algorithms=['RS256'],\n            audience='api://corporate-gateway', issuer='https://auth.company.com/'\n        )\n        return payload\n    except jwt.ExpiredSignatureError:\n        return {'error': 'Token Expired'}\n    except jwt.InvalidTokenError:\n        return {'error': 'Invalid Signature'}"
                }
            ],
            "practice_questions": [
                {
                    "question": "Which OAuth 2.0 flow is officially mandated by IETF best practices for Single Page Applications (React/Vue) and mobile native apps to prevent authorization code interception?",
                    "options": [
                        "Implicit Flow",
                        "Resource Owner Password Credentials Grant",
                        "Authorization Code Grant with PKCE",
                        "SAML 1.1 Web SSO"
                    ],
                    "answer": "Authorization Code Grant with PKCE",
                    "explanation": "The Authorization Code Flow with PKCE (Proof Key for Code Exchange) prevents attackers from stealing the authorization code in public clients (browsers/mobile devices) by verifying a cryptographic secret (code_verifier) during the token exchange step."
                }
            ],
            "interview_questions": [
                {
                    "company": "Okta & Microsoft",
                    "question": "What is the core principle of Zero Trust Architecture, and why has it replaced traditional perimeter-based network security?",
                    "model_answer": "Traditional perimeter security assumes that any user or device inside the corporate internal network is trustworthy ('Castle and Moat'). Once an attacker breaches the VPN or compromises one workstation, they can move laterally unrestricted. Zero Trust operates on the principle of 'Never Trust, Always Verify'. Every single request, whether originating inside or outside the network, must be authenticated, authorized, and encrypted based on user identity, device health, and context.",
                    "interviewer_tip": "Highlight lateral movement prevention and micro-segmentation."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Security Operations Center (SOC), SIEM, Threat Hunting & Incident Response",
        "key_takeaways": "Master Security Information and Event Management (SIEM), log correlation, incident response lifecycle (NIST 800-61), and containment playbooks.",
        "topics": [
            "SOC Operations: Tier 1 (Triage), Tier 2 (Investigation), Tier 3 (Threat Hunting & Forensics)",
            "SIEM Architecture (Splunk, Elastic SIEM, Microsoft Sentinel): Log ingestion, parsing, correlation rules & alerts",
            "Incident Response Lifecycle (NIST SP 800-61): Preparation, Detection & Analysis, Containment, Eradication, Recovery, Lessons Learned",
            "Indicators of Compromise (IoC) vs Indicators of Attack (IoA) and YARA / Sigma rules",
            "Ransomware & Data Breach containment playbooks: Network isolation, credential revocation & memory forensics"
        ],
        "sections": {
            "concept": "A Security Operations Center (SOC) provides continuous monitoring, detection, and response against cyber incidents. A SIEM (Security Information and Event Management) system centralizes billions of logs daily across servers, network firewalls, Active Directory, and cloud services, evaluating correlation rules to detect anomalous behavior (e.g. an account logging in from India and the UK within 5 minutes\u2014an impossible travel alert). Incident response adheres strictly to the NIST SP 800-61 standard. When responding to ransomware, the first imperative is immediate network containment (disabling switch ports and revoking API keys) before analyzing Volatility memory dumps.",
            "formulas": "1. Mean Time to Detect (MTTD) = Sum(Detection_Time - Compromise_Time) / Total_Incidents\n2. Mean Time to Respond (MTTR) = Sum(Containment_Time - Detection_Time) / Total_Incidents\n3. False Positive Rate (FPR) = False_Positives / (False_Positives + True_Negatives)",
            "solved_examples": [
                {
                    "title": "Writing a SIEM Correlation Query in Splunk / KQL to Detect Impossible Travel",
                    "difficulty": "Medium | Splunk, CrowdStrike, Deloitte",
                    "problem": "Write a query that alerts when a single user account logs in from two geographic locations over 1,000 miles apart within a 15-minute window.",
                    "step_by_step": [
                        "Step 1: Filter successful authentication events: `EventID == 4624`.",
                        "Step 2: Group events by `User` over a 15-minute tumbling window.",
                        "Step 3: Extract source IP latitude and longitude using GeoIP lookups.",
                        "Step 4: Calculate geographic distance and travel speed required.",
                        "Step 5: Trigger high-severity alert if implied velocity exceeds 600 mph (commercial flight speed)."
                    ],
                    "code_or_math": "# Conceptual Splunk SPL / KQL Logic\nSigninLogs\n| where ResultType == 0\n| summarize Locations=makeset(Location), IPs=makeset(IPAddress) by UserPrincipalName, bin(TimeGenerated, 15m)\n| where array_length(Locations) > 1"
                }
            ],
            "practice_questions": [
                {
                    "question": "In the NIST SP 800-61 Incident Response framework, which phase immediately follows 'Detection & Analysis'?",
                    "options": [
                        "Lessons Learned",
                        "Containment, Eradication & Recovery",
                        "Preparation",
                        "Public Press Release"
                    ],
                    "answer": "Containment, Eradication & Recovery",
                    "explanation": "Once a cyber threat is detected and analyzed, the immediate next phase is Containment (preventing the incident from spreading), followed by Eradication (removing malware/artifacts) and Recovery (restoring clean systems to normal operations)."
                }
            ],
            "interview_questions": [
                {
                    "company": "CrowdStrike & Mandiant",
                    "question": "What is the difference between an Indicator of Compromise (IoC) and an Indicator of Attack (IoA)?",
                    "model_answer": "An Indicator of Compromise (IoC) is forensic evidence left behind after an attack has occurred (such as a known malware MD5 file hash, a malicious IP address, or a specific registry key modification). An Indicator of Attack (IoA) focuses on the real-time intent and behavior of the attacker as the attack is happening (such as lateral movement via PowerShell, process hollowing, or credential dumping from LSASS memory), regardless of what specific malware binary is used.",
                    "interviewer_tip": "Connect IoAs to modern behavioral endpoint detection and response (EDR) systems."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Vulnerability Assessment, Penetration Testing & Ethical Hacking",
        "key_takeaways": "Master the ethical hacking methodology: Reconnaissance, Scanning (Nmap), Vulnerability Analysis, Exploitation (Metasploit), and Post-Exploitation.",
        "topics": [
            "Penetration Testing methodologies: PTES, OSSTMM, Black-Box vs White-Box vs Gray-Box testing",
            "Reconnaissance & OSINT: Shodan, WHOIS, DNS harvesting, sublist3r & theHarvester",
            "Network Scanning with Nmap: SYN stealth scan (-sS), service versioning (-sV), OS detection (-O) & NSE scripts",
            "Vulnerability scanning with Nessus, Qualys & OpenVAS: CVSS v3.1 scoring metrics",
            "Exploitation frameworks (Metasploit), Privilege Escalation (Linux SUID / Windows tokens) & Reporting"
        ],
        "sections": {
            "concept": "Penetration testing is the authorized simulated cyberattack against computer systems to evaluate security posture before malicious actors exploit weaknesses. The Penetration Testing Execution Standard (PTES) defines seven phases: Pre-engagement, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post-Exploitation, and Reporting. Network scanning with Nmap maps open ports and identifies vulnerable service versions. Vulnerabilities are ranked by the Common Vulnerability Scoring System (CVSS v3.1), assessing Attack Vector, Complexity, Privileges Required, User Interaction, Scope, and CIA impact.",
            "formulas": "1. CVSS v3.1 Base Score: Derived from Exploitability Metrics x Impact Metrics (Scale 0.0 to 10.0)\n2. CVSS Severity Ratings: Low (0.1-3.9), Medium (4.0-6.9), High (7.0-8.9), Critical (9.0-10.0)\n3. Nmap SYN Scan Flag: TCP Header with SYN=1, ACK=0 (Half-Open scanning avoids full TCP connection logging)",
            "solved_examples": [
                {
                    "title": "Executing and Interpreting an Nmap Advanced Port and Vulnerability Scan",
                    "difficulty": "Medium | OffSec (OSCP), Mandiant, Rapid7",
                    "problem": "Write an Nmap command to scan a target server for top ports, detect service versions, run default vulnerability scripts, and output findings.",
                    "step_by_step": [
                        "Step 1: Use `-sS` for fast TCP SYN stealth scan without completing 3-way handshakes.",
                        "Step 2: Use `-sV` to probe open ports to determine exact service names and version numbers.",
                        "Step 3: Use `-sC` to run standard Nmap Scripting Engine (NSE) vulnerability detection scripts.",
                        "Step 4: Use `-T4` for aggressive speed timing.",
                        "Step 5: Use `-oA target_audit` to save output in text, XML, and grepable formats simultaneously."
                    ],
                    "code_or_math": "# Professional Nmap Vulnerability Assessment Command\nnmap -sS -sV -sC -T4 -p 1-10000 -oA network_audit_report 192.168.1.50"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary characteristic of a 'Gray-Box' penetration test?",
                    "options": [
                        "The tester has zero knowledge and zero access credentials ahead of time",
                        "The tester is provided partial knowledge, such as standard user login credentials or network architecture diagrams",
                        "The test is performed only on weekends",
                        "The tester is given full source code and root administrative access"
                    ],
                    "answer": "The tester is provided partial knowledge, such as standard user login credentials or network architecture diagrams",
                    "explanation": "In a Gray-Box test, the security auditor is provided partial knowledge or limited user-level privileges, simulating an attack by an authenticated insider or an attacker who has already breached the perimeter."
                }
            ],
            "interview_questions": [
                {
                    "company": "Mandiant & Deloitte Cyber",
                    "question": "What is the difference between a Vulnerability Assessment and a Penetration Test?",
                    "model_answer": "A Vulnerability Assessment is a broad, typically automated scan (using Nessus or Qualys) designed to identify, catalog, and rank known vulnerabilities and missing patches across a large network without exploiting them. A Penetration Test goes a step further: an ethical hacker manually attempts to safely exploit those vulnerabilities to prove real-world business risk, bypass security defenses, pivot laterally, and extract proof of concept data.",
                    "interviewer_tip": "Highlight that penetration tests demonstrate exploitability and business impact."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Solved Cybersecurity Case Studies & Placement Technical Scenarios",
        "key_takeaways": "Master resolving complex enterprise security incidents: Equifax Apache Struts exploit, SolarWinds supply chain breach, and credential stuffing defense.",
        "topics": [
            "Case Study 1: Dissecting the SolarWinds Supply Chain Attack and software build pipeline security",
            "Case Study 2: The Equifax Breach: Apache Struts OGNL injection and failure to patch critical CVEs",
            "Case Study 3: Mitigating Distributed Credential Stuffing attacks against high-traffic banking portals",
            "DevSecOps: SAST, DAST, SCA (Software Composition Analysis) & container image scanning in CI/CD",
            "FAANG & Defense Cybersecurity placement interview questions, scenario drills & grading matrices"
        ],
        "sections": {
            "concept": "Campus placement interviews for Cybersecurity Engineer, Security Analyst, and SOC Specialist roles test real-world forensic diagnosis and remediation architecture. The SolarWinds breach highlighted software supply chain vulnerabilities: attackers injected malicious backdoor code (SUNBURST) directly into the vendor's build pipeline, signing it with valid digital certificates. DevSecOps integrates automated security guardrails directly into CI/CD pipelines: Static Application Security Testing (SAST) scans source code for bugs; Software Composition Analysis (SCA) detects vulnerable open-source dependencies (CVEs); Dynamic Application Security Testing (DAST) tests running staging applications for runtime vulnerabilities.",
            "formulas": "1. Mean Time to Remediate (MTTR): Time elapsed from vulnerability disclosure to production patch deployment\n2. Credential Stuffing Failure Rate: Legitimate logins ~95% success; Credential stuffing attacks ~98% failure rate\n3. Dependency Vulnerability Depth: Total_CVEs = Direct_Dependencies + Transitive_Dependencies",
            "solved_examples": [
                {
                    "title": "Architecting a Multi-Layered Defense Against Credential Stuffing Attacks",
                    "difficulty": "Hard | Cloudflare, Akamai, PayPal",
                    "problem": "An online retail site experiences a credential stuffing attack of 2,000,000 automated login attempts per hour using leaked breach databases.",
                    "step_by_step": [
                        "Step 1: Edge Defense: CloudFront WAF with Bot Control detects automated headless browsers (Puppeteer/Selenium).",
                        "Step 2: IP Reputation: Block known Tor exit nodes, public proxies, and botnet IP ranges.",
                        "Step 3: Adaptive Rate Limiting: Restrict failed attempts per IP and per username to 5 per minute.",
                        "Step 4: Behavioral Challenge: Present invisible WebAuthn or Turnstile challenges when bot probability exceeds threshold.",
                        "Step 5: Breach Credential Checking: Check password hashes against HaveIBeenPwned API during login and mandate password resets for compromised credentials."
                    ],
                    "code_or_math": "# Bot Score & Credential Stuffing Filter Logic\ndef evaluate_login_risk(ip, username, bot_score, failed_attempts_last_min):\n    if bot_score > 0.8 or failed_attempts_last_min > 5:\n        return 'CHALLENGE_OR_BLOCK'\n    return 'ALLOW_VERIFICATION'"
                }
            ],
            "practice_questions": [
                {
                    "question": "Which DevSecOps tool analyzes third-party open source packages and libraries in your package.json or requirements.txt to detect known CVE vulnerabilities and license risks?",
                    "options": [
                        "Static Application Security Testing (SAST)",
                        "Software Composition Analysis (SCA)",
                        "Dynamic Application Security Testing (DAST)",
                        "Interactive Application Security Testing (IAST)"
                    ],
                    "answer": "Software Composition Analysis (SCA)",
                    "explanation": "Software Composition Analysis (SCA) tools (like Snyk, Dependabot, and OWASP Dependency-Check) scan open-source dependencies and third-party libraries for publicly disclosed CVE vulnerabilities and licensing non-compliance."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Google",
                    "question": "What is the difference between SAST and DAST in a modern CI/CD pipeline?",
                    "model_answer": "SAST (Static Application Security Testing) is white-box testing that analyzes source code or compiled binaries from the inside without executing the program, identifying flaws like hardcoded secrets and SQL concatenation early in the development lifecycle. DAST (Dynamic Application Security Testing) is black-box testing that evaluates a running application from the outside, finding runtime issues like configuration errors, cookie security flags, and real-world injection vulnerabilities.",
                    "interviewer_tip": "Explain that mature DevSecOps pipelines run both SAST during code commit and DAST during staging deployment."
                }
            ]
        }
    }
]
