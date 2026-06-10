# Project Context — VAPT Thesis on neuralsh.com

## What this project is
This is a graduation thesis for an internship at **Prestige Alliance**, documenting a black-box Vulnerability Assessment and Penetration Testing (VAPT) engagement on **neuralsh.com**.

## Current status
The thesis is **complete** in Markdown. The next task is to rewrite it into a **Microsoft Word (.docx)** document following ITC thesis format rules (A4, Times New Roman 12pt, 1.5 line spacing, chapter headings, proper table of contents).

## Key files in this folder
| File | Description |
|------|-------------|
| `THESIS_VAPT_FULL.md` | Full thesis — 13 chapters, ~13,000 words, neuralsh.com only |
| `VAPT_REPORT_neuralsh.html` | Professional HTML VAPT report (78KB) |
| `VAPT_REPORT_neuralsh.pdf` | PDF version of the report (854KB) |
| `ATTACK_CHAIN_DIAGRAM.html` | Attack chain diagram — 4 chains, SVG infrastructure map |
| `ATTACK_CHAIN_DIAGRAM.pdf` | PDF version of attack chain diagram |
| `ACTION_PLAN.html` | Gantt-style internship action plan (Feb–May) |
| `ACTION_PLAN.pdf` | PDF version of action plan |

## Target summary — neuralsh.com
- AI-powered neural search platform
- Nuxt.js frontend behind Cloudflare CDN
- Origin server: 103.16.62.217 (Cloudways shared hosting, cprapid.com)
- **17 findings total: 4 Critical, 4 High, 6 Medium, 3 Low**
- 2 chains confirmed exploited: Rate Limit Bypass (50/50 tokens, 0 rate-limit responses) and JWT token farming

## 17 Findings summary
| ID | Title | Severity | CVSS |
|----|-------|----------|------|
| N-001 | WHM Admin Panel Publicly Exposed | Critical | 10.0 |
| N-002 | MySQL Port Exposed to Internet | Critical | 9.8 |
| N-013 | MikroTik RouterOS Admin Panel Exposed | Critical | 9.6 |
| N-014 | Cloudflare WAF Bypass via Origin IP Disclosure | Critical | 9.1 |
| N-005 | Authentication Rate Limiting Bypass (X-Forwarded-For) | High | 8.6 |
| N-007 | JWT Token Farming via Unauthenticated Endpoint | High | 8.1 |
| N-015 | Shared Hosting Lateral Movement Risk | High | 7.8 |
| N-016 | cPanel Exposed on Non-Standard Port | High | 7.5 |
| N-003 | Missing Security Headers (CSP, HSTS, X-Frame) | Medium | 6.5 |
| N-004 | Webmail Interface Publicly Accessible | Medium | 6.2 |
| N-006 | Excessive CORS Permissiveness on API | Medium | 6.1 |
| N-008 | PowerDNS Admin Interface Exposed | Medium | 5.9 |
| N-009 | SSL Certificate Leaks Infrastructure Details | Medium | 5.4 |
| N-010 | DNS Wildcard Enables Subdomain Takeover Risk | Medium | 5.3 |
| N-011 | Email Security Misconfiguration (DMARC p=none) | Low | 3.8 |
| N-012 | Server Version Disclosure via HTTP Headers | Low | 3.5 |
| N-017 | Directory Listing Enabled on Origin Server | Low | 3.1 |

## Attack chains
1. **Chain 1 — WHM Server Compromise**: Cloudflare bypass → origin IP → WHM admin panel exposed → unauthenticated access to full server
2. **Chain 2 — Rate Limit Bypass** *(Confirmed exploited)*: X-Forwarded-For spoof → 50 auth requests, 0 rate-limit responses → JWT token farming
3. **Chain 3 — MikroTik Network Takeover**: Origin IP scan → port 8291/8728 open → MikroTik Winbox/API exposed → full network device control
4. **Chain 4 — MySQL Data Exfiltration**: Origin IP → port 3306 open → MySQL internet-facing → credential brute-force risk → full DB access

## ITC thesis format rules (for Word document)
- Paper: A4
- Font: Times New Roman 12pt body, 14pt Chapter headings, 13pt section headings
- Spacing: 1.5 line spacing throughout
- Margins: 3cm left, 2.5cm right/top/bottom
- Chapter headings: bold, centered or left-aligned, numbered (Chapter 1, 1.1, 1.1.1)
- No contractions (don't → do not, can't → cannot)
- Past tense for methodology/findings
- Tables: centered, captioned below ("Table X: Description")
- Figures: centered, captioned below ("Figure X: Description")
- References: APA 7th edition
- Page numbers: bottom center, Roman numerals for front matter, Arabic from Chapter 1

## Thesis chapter structure
1. Introduction (Background, Problem Statement, Objectives, Scope, Organisation)
2. Literature Review (Web App Security, Frameworks, Vuln Classes, CVSS, Related Work)
3. Research Methodology (Design, Testing Approach, Tools, Phases, Evidence, Ethics)
4. Target Profile and Scope
5. Phase 1 — Reconnaissance
6. Phase 2 — Scanning and Enumeration
7. Phase 3 — Vulnerability Assessment
8. Phase 4 — Exploitation
9. Phase 5 — Post-Exploitation
10. Findings Analysis (17 findings table + CVSS breakdown)
11. Attack Chain Analysis
12. Remediation Roadmap
13. Conclusion
+ References + Appendices (A–H)

## What to do next (Word document task)
Convert `THESIS_VAPT_FULL.md` into a properly formatted `.docx` file:
- Apply ITC format (font, spacing, margins above)
- Generate proper Table of Contents
- Format the 17-findings table and all code blocks
- Insert Figure/Table captions
- Add page numbers
- Use the Scope of Engagement text (Prestige Alliance as authorizing organization)
- The action plan tables (Feb–Mar, Apr–May Gantt) should appear in section 6 of the thesis intro/proposal section
