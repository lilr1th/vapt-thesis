#!/usr/bin/env python3
"""
generate_docx.py — VAPT Thesis to Word (.docx) Converter
SE_LYTHENG-style finding cards + ITC format (A4, TNR 12pt, 1.5 spacing)

Requirements: pip install python-docx
Run from the thesis folder.
"""
import os, re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE  = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(BASE, "screenshots")
IMGS  = os.path.join(BASE, "image")
MD    = os.path.join(BASE, "THESIS_VAPT_FULL.md")
OUT   = os.path.join(BASE, "THESIS_VAPT_WORD.docx")

# ── Color palette (bg_hex, text_hex) ─────────────────────────────────────────
C = {
    "critical": ("8B0000", "FFFFFF"),
    "high":     ("C00000", "FFFFFF"),
    "medium":   ("FFC000", "000000"),
    "low":      ("70AD47", "FFFFFF"),
    "label":    ("D9D9D9", "000000"),
    "blue":     ("2E74B5", "FFFFFF"),
}

def hex2rgb(h):
    return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

def set_bg(cell, fill_hex):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    for s in tcPr.findall(qn('w:shd')):
        tcPr.remove(s)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_vert(cell, val='center'):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    vAlign = OxmlElement('w:vAlign')
    vAlign.set(qn('w:val'), val)
    tcPr.append(vAlign)

# ── Document helpers ──────────────────────────────────────────────────────────
def new_doc():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width    = Cm(21.0)
    sec.page_height   = Cm(29.7)
    sec.left_margin   = Cm(3.0)
    sec.right_margin  = Cm(2.5)
    sec.top_margin    = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sty = doc.styles['Normal']
    sty.font.name = 'Times New Roman'
    sty.font.size = Pt(12)
    sty.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    sty.paragraph_format.space_after = Pt(6)
    return doc

def fmt(run, size=12, bold=False, italic=False, color=None):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = hex2rgb(color)

def body(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=1.27,
         size=12, bold=False, italic=False):
    if not text or not text.strip():
        return
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.first_line_indent = Cm(indent)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text.strip())
    fmt(r, size=size, bold=bold, italic=italic)
    return p

def ch_head(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.page_break_before = True
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    r = p.add_run(text)
    fmt(r, size=14, bold=True)

def sec_head(doc, text, level=1):
    size = 13 if level == 1 else 12
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    r = p.add_run(text)
    fmt(r, size=size, bold=True)

def fig_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.first_line_indent = Cm(0)
    r = p.add_run(text)
    fmt(r, size=10, italic=True)

def add_img(doc, path, caption, w=14.0):
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.add_run().add_picture(path, width=Cm(w))
        fig_caption(doc, caption)
    else:
        p = doc.add_paragraph(f'[FIGURE — {caption}]')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)

def code_block(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(1.27)
    p.paragraph_format.right_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.first_line_indent = Cm(0)
    r = p.add_run(text)
    r.font.name = 'Courier New'
    r.font.size = Pt(9)

def md_table(doc, rows_data):
    if not rows_data:
        return
    ncols = len(rows_data[0])
    tbl = doc.add_table(rows=len(rows_data), cols=ncols)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row in enumerate(rows_data):
        for ci, cell_txt in enumerate(row):
            cell = tbl.cell(ri, ci)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(cell_txt.strip())
            fmt(r, size=11, bold=(ri==0))
            if ri == 0:
                set_bg(cell, C['blue'][0])
                r.font.color.rgb = hex2rgb(C['blue'][1])
    doc.add_paragraph()

# ── Finding Card (SE_LYTHENG style) ──────────────────────────────────────────
def finding_card(doc, f):
    sev = f['severity'].lower()
    fill, txt = C[sev]

    sec_head(doc, f"{f['id']} — {f['title']}", level=2)

    tbl = doc.add_table(rows=8, cols=3)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    for row in tbl.rows:
        row.cells[0].width = Cm(3.4)
        row.cells[1].width = Cm(5.8)
        row.cells[2].width = Cm(5.8)

    # Row 0 — severity badge (all 3 merged)
    c0 = tbl.cell(0, 0)
    c0.merge(tbl.cell(0, 2))
    badge = f"{f['severity'].upper()}   CVSS {f['cvss']}   {f['id']}: {f['title']}"
    if f.get('status') == 'Exploited':
        badge += "   [CONFIRMED EXPLOITED]"
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = p0.add_run(badge)
    fmt(r0, size=11, bold=True, color=txt)
    set_bg(c0, fill)
    set_cell_vert(c0)

    def lv(ri, lbl, val):
        """Label | merged value row"""
        lc = tbl.cell(ri, 0)
        vc = tbl.cell(ri, 1)
        vc.merge(tbl.cell(ri, 2))
        set_bg(lc, C['label'][0])
        set_cell_vert(lc)
        rl = lc.paragraphs[0].add_run(lbl)
        fmt(rl, size=11, bold=True)
        rv = vc.paragraphs[0].add_run(val)
        fmt(rv, size=11)

    def ll(ri, lbl, items):
        """Label | merged value with numbered list"""
        lc = tbl.cell(ri, 0)
        vc = tbl.cell(ri, 1)
        vc.merge(tbl.cell(ri, 2))
        set_bg(lc, C['label'][0])
        set_cell_vert(lc)
        fmt(lc.paragraphs[0].add_run(lbl), size=11, bold=True)
        for i, item in enumerate(items):
            p_ = vc.paragraphs[0] if i == 0 else vc.add_paragraph()
            fmt(p_.add_run(f"{i+1}.  {item}"), size=11)

    # Row 1 — Description
    lv(1, "Description:", f['description'])

    # Row 2 — Risks: two colored side-by-side cells
    lc2 = tbl.cell(2, 0)
    lk  = tbl.cell(2, 1)
    rk  = tbl.cell(2, 2)
    set_bg(lc2, C['label'][0])
    set_cell_vert(lc2)
    fmt(lc2.paragraphs[0].add_run("Risks:"), size=11, bold=True)

    lsev = f['likelihood'].lower()
    lf, lt = C.get(lsev, C['medium'])
    set_bg(lk, lf)
    set_cell_vert(lk)
    plk = lk.paragraphs[0]
    plk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fmt(plk.add_run(f"Likelihood: {f['likelihood']}"), size=11, bold=True, color=lt)

    set_bg(rk, fill)
    set_cell_vert(rk)
    prk = rk.paragraphs[0]
    prk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fmt(prk.add_run(f"Risk Rating: {f['risk_rating']}"), size=11, bold=True, color=txt)

    # Rows 3–7
    lv(3, "Impact:",       f['impact'])
    lv(4, "Tool Used:",    f['tool'])
    ll(5, "References:",   f['references'])
    lv(6, "Remediation:",  f['remediation'])
    lv(7, "Evidence:",     f['evidence'])

    doc.add_paragraph()

# ── All 20 findings ───────────────────────────────────────────────────────────
FINDINGS = [
  { "id":"N-001","severity":"Critical","cvss":"9.8","risk_rating":"Critical",
    "title":"MySQL Port 3306 Exposed to Internet",
    "host":"103.16.62.217:3306","tool":"Nmap, mysql-client",
    "likelihood":"High","status":"Confirmed",
    "description":"The MySQL 8.0.43 database server is directly accessible from the public internet on port 3306, accepting full TCP connections from any external IP address. An attacker does not need to compromise the web application to reach the database — they can attempt authentication directly at the database layer, bypassing all application-level access controls. No rate limiting or IP-based blocking exists at the database layer.",
    "impact":"Successful access grants full read and write access to all application databases, potentially including user records, session data, and API secrets. MySQL's User Defined Function (UDF) feature could further be abused to achieve remote command execution on the underlying server.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-2122"],
    "remediation":"Restrict port 3306 to localhost or a trusted management VPN via firewall rules. Never expose database ports to the public internet under any circumstances.",
    "evidence":"Figure 4.9 — Nmap scan confirming 3306/tcp open mysql MySQL 8.0.43; Figure 4.19 — MySQL connection attempt from public IP showing authentication prompt" },

  { "id":"N-002","severity":"Critical","cvss":"9.1","risk_rating":"Critical",
    "title":"MikroTik Admin Panel Exposed (Port 9001)",
    "host":"103.16.62.217:9001","tool":"Nmap, curl, browser",
    "likelihood":"High","status":"Confirmed",
    "description":"The MikroTik RouterOS web configuration interface (WebFig) is publicly accessible on port 9001, returning HTTP 200 with a fully rendered login page. The login form pre-fills 'admin' as the default username. MikroTik devices ship with a factory default of admin/blank password — if this default has not been changed, full network device control is available without any credential knowledge.",
    "impact":"An attacker with RouterOS access can modify routing tables, capture all network traffic in promiscuous mode, create persistent backdoor accounts, remove all firewall rules, and disrupt all hosted services on the server.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://nvd.nist.gov/vuln/detail/CVE-2018-14847"],
    "remediation":"Restrict port 9001 to a trusted management IP via firewall. Change MikroTik default credentials immediately. Disable unused RouterOS services (telnet, FTP, API).",
    "evidence":"Figure 4.11 — curl response confirming RouterOS WebFig accessible; Figure 4.18 — Browser showing MikroTik WebFig login with admin pre-filled" },

  { "id":"N-013","severity":"Critical","cvss":"9.8","risk_rating":"Critical",
    "title":"cPanel Admin Panel Exposed (Port 2083)",
    "host":"103.16.62.217:2083","tool":"Nmap, curl",
    "likelihood":"High","status":"Confirmed",
    "description":"The cPanel web hosting control panel is publicly accessible on port 2083 with no IP restriction and no two-factor authentication prompt. cPanel provides full management of the hosting account including file manager (read and write all web application files), database management via phpMyAdmin, email account control, FTP credential creation, and subdomain configuration.",
    "impact":"A password reset link is present on the login page. If an attacker compromises the registered email account, they can reset the cPanel password and gain full hosting account access without brute force. All application files and databases become accessible.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://docs.cpanel.net/cpanel/security/two-factor-authentication-for-cpanel/"],
    "remediation":"Restrict port 2083 to trusted management IPs via Cloudways firewall. Enable two-factor authentication on cPanel immediately.",
    "evidence":"Figure 4.10 — curl response showing cPanel Login title confirming public accessibility" },

  { "id":"N-014","severity":"Critical","cvss":"10.0","risk_rating":"Critical",
    "title":"WHM Root Panel Exposed (Port 2087)",
    "host":"103.16.62.217:2087","tool":"Nmap, curl, browser",
    "likelihood":"High","status":"Confirmed",
    "description":"WHM (Web Host Manager) is the root-level server administration panel for cPanel-based servers. It is publicly accessible on port 2087 with no IP restriction, no two-factor authentication, and no account lockout. WHM access is functionally equivalent to root shell access: it provides a built-in Terminal feature, full server configuration control, and administrative access to every hosted account on the server.",
    "impact":"An attacker who gains WHM access compromises not only neuralsh.com but every other hosted domain on the shared server simultaneously. This is the highest-severity finding in the engagement, receiving the maximum CVSS score of 10.0.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://docs.cpanel.net/whm/security-center/"],
    "remediation":"Immediately firewall port 2087 to trusted IPs only. This single action eliminates the highest-risk vector in the entire engagement.",
    "evidence":"Figure 4.17 — Browser showing WHM login page at 103.16.62.217:2087 (SSL warning visible, no authentication bypass required)" },

  { "id":"N-003","severity":"High","cvss":"7.2","risk_rating":"High",
    "title":"SSH Port 22 Publicly Accessible",
    "host":"103.16.62.217:22","tool":"Nmap, ssh",
    "likelihood":"Medium","status":"Confirmed",
    "description":"OpenSSH 8.9p1 is publicly accessible on port 22. SSH key-based authentication was confirmed as the enforced method for tested usernames, which reduces the immediate exploitation risk. However, the port remains exposed to brute-force attempts for any account that may have password authentication enabled.",
    "impact":"The SMTP banner confirms this is a cPanel shared hosting server where the primary user typically has sudo privileges. Successful SSH compromise is equivalent to root access to the entire server and all co-hosted accounts.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://www.sans.org/security-resources/policies/general/pdf/remote-access-policy"],
    "remediation":"Enforce PasswordAuthentication no in /etc/ssh/sshd_config. Install fail2ban with aggressive thresholds. Restrict SSH to a trusted management IP via firewall.",
    "evidence":"Figure 4.9 — Nmap scan confirming 22/tcp open OpenSSH 8.9p1" },

  { "id":"N-004","severity":"High","cvss":"7.5","risk_rating":"High",
    "title":"Shared Hosting Lateral Movement Risk",
    "host":"103.16.62.217 (shared infrastructure)","tool":"openssl, curl",
    "likelihood":"Medium","status":"Confirmed",
    "description":"The origin server is a shared cPanel hosting environment (Cloudways/cprapid.com) hosting multiple clients on the same physical server. SSL certificates issued to *.onesala.com and www.endoncambodia.com confirmed the presence of other tenants. On shared cPanel hosting, a single WHM-level compromise grants access to the files, databases, and email of every co-hosted account simultaneously.",
    "impact":"A compromise of neuralsh.com's hosting account constitutes a data breach affecting organizations that have no relationship with neuralsh.com and no awareness of its security posture, creating third-party data protection liability.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://cheatsheetseries.owasp.org/cheatsheets/Infrastructure_as_Code_Security_Cheat_Sheet.html"],
    "remediation":"Migrate neuralsh.com to a dedicated server or isolated cloud instance. In the short term, ensure WHM is firewalled immediately to eliminate the most direct lateral movement path.",
    "evidence":"Figure 4.8 — SSL certificate showing onesala.com and endoncambodia.com on same origin server" },

  { "id":"N-005","severity":"High","cvss":"9.1","risk_rating":"High",
    "title":"Rate Limit Bypass via X-Forwarded-For Header Spoofing",
    "host":"neuralsh.com/web/v1/init/token","tool":"Burp Suite, curl, Python script",
    "likelihood":"High","status":"Exploited",
    "description":"The application's rate-limiting mechanism uses the client-supplied X-Forwarded-For header as the identifier for tracking request rates per IP address. Because X-Forwarded-For is fully controllable by the client, an attacker can supply a different random IP value on each request, making every request appear to originate from a unique source and bypassing the rate limit entirely.",
    "impact":"Exploitation was confirmed with a 100% success rate: 50 consecutive requests were sent with rotating X-Forwarded-For values and all 50 received HTTP 200 responses — not a single rate-limit response was returned. This bypass enables unlimited JWT token farming and applies to any endpoint using the same IP-tracking logic. CONFIRMED EXPLOITED.",
    "references":["https://owasp.org/Top10/A04_2021-Insecure_Design/","https://developers.cloudflare.com/fundamentals/reference/http-headers/"],
    "remediation":"Replace X-Forwarded-For with Cloudflare's CF-Connecting-IP header for all rate-limiting logic. CF-Connecting-IP is set by Cloudflare and cannot be spoofed by the client.",
    "evidence":"Figure 4.15 — Burp Suite showing 50/50 requests returning HTTP 200 with rotating X-Forwarded-For headers; 0 rate-limit responses" },

  { "id":"N-015","severity":"High","cvss":"7.5","risk_rating":"High",
    "title":"Webmail Interface Exposed (Port 2096)",
    "host":"103.16.62.217:2096","tool":"Nmap, curl",
    "likelihood":"Medium","status":"Confirmed",
    "description":"The cPanel Webmail login interface is publicly accessible on port 2096 without IP restriction. This interface allows brute-force attacks against all email accounts hosted on the server, including @neuralsh.com addresses.",
    "impact":"A compromised email account can be used to trigger password reset flows for other services (cPanel, application accounts) and to send phishing emails from a legitimate @neuralsh.com address with valid DKIM signatures.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://docs.cpanel.net/cpanel/email/webmail/"],
    "remediation":"Restrict port 2096 to trusted IPs via firewall. Enforce strong passwords on all email accounts. Implement CAPTCHA or account lockout on the webmail login.",
    "evidence":"Nmap scan — 2096/tcp open confirming cPanel Webmail public accessibility" },

  { "id":"N-018","severity":"High","cvss":"7.5","risk_rating":"High",
    "title":"Additional cPanel Interfaces Exposed (Ports 2078, 2091)",
    "host":"103.16.62.217:2078, 2091","tool":"Nmap, curl (follow-up scan 10 June 2026)",
    "likelihood":"Medium","status":"Confirmed",
    "description":"Ports 2078 and 2091 were not present in the June 6 baseline scan but appeared open in the June 10 follow-up scan, both returning HTTP 401 with WWW-Authenticate: Basic realm=Restricted Area. These are additional cPanel management service ports. Their appearance after the initial scan indicates infrastructure changes are being made without a security review process.",
    "impact":"These ports represent additional credential brute-force attack surface for server management interfaces. The unexplained appearance of new open ports also suggests absence of change management controls.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
    "remediation":"Restrict ports 2078 and 2091 via firewall. Conduct a full port audit of 103.16.62.217 and close all ports without a documented business purpose.",
    "evidence":"Follow-up Nmap scan (10 June 2026) — 2078/tcp and 2091/tcp open returning HTTP 401" },

  { "id":"N-006","severity":"Medium","cvss":"5.3","risk_rating":"Medium",
    "title":"API Routes Exposed in Client-Side JavaScript",
    "host":"neuralsh.com/_nuxt/","tool":"curl, grep",
    "likelihood":"Low","status":"Confirmed",
    "description":"The complete API route structure of the application is disclosed in the compiled Nuxt.js JavaScript bundle. Routes including /web/v1/init/token, /web/v1/text/search, /web/v1/image/search, /web/v1/report/save, and /api/geocode were extracted directly from the bundle without any authentication or directory scanning.",
    "impact":"This reconnaissance eliminated the need for directory brute force and directly enabled the targeted exploitation of the unauthenticated token endpoint (N-007). Every internal API endpoint is effectively public knowledge.",
    "references":["https://owasp.org/Top10/A01_2021-Broken_Access_Control/"],
    "remediation":"Minimize unnecessary route exposure in the bundle. Implement an API gateway with strict allowlisting. Treat all API endpoints as public knowledge and secure them with proper authentication regardless of whether they appear in client code.",
    "evidence":"curl extraction of API routes from /_nuxt/Bpuv52g-.js bundle" },

  { "id":"N-007","severity":"Medium","cvss":"5.3","risk_rating":"Medium",
    "title":"Unauthenticated JWT Token Issuance",
    "host":"neuralsh.com/web/v1/init/token","tool":"curl, CyberChef, hashcat, Burp Suite",
    "likelihood":"High","status":"Exploited",
    "description":"The token endpoint issues a valid signed JWT token to any unauthenticated caller with no credentials, API key, device fingerprint, or identifying information required. Tokens carry a type:guest claim and a 30-minute validity window. A follow-up verification on 11 June 2026 confirmed the endpoint remains live and returning HTTP 200 — no remediation has been applied.",
    "impact":"Using the rate-limit bypass from N-005, 50 valid tokens were farmed in approximately three seconds. Each token granted real API access to search and category endpoints. JWT secret brute-force against rockyou.txt (14,344,391 candidates) was unsuccessful; however, token farming impact is independent of secret strength. CONFIRMED EXPLOITED.",
    "references":["https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/","https://portswigger.net/web-security/jwt"],
    "remediation":"Require a browser-computed fingerprint, Cloudflare Turnstile challenge, or origin header validation before issuing tokens. Implement token binding to prevent reuse outside the originating browser session.",
    "evidence":"Figure 4.15 — 50 tokens collected; Figure 4.16 — endpoint confirmed live (HTTP 200) as of 11 June 2026" },

  { "id":"N-008","severity":"Medium","cvss":"5.9","risk_rating":"Medium",
    "title":"SSL Certificate Mismatch on Backend Server",
    "host":"103.16.62.217:443, 110, 143, 465","tool":"openssl",
    "likelihood":"Low","status":"Confirmed",
    "description":"The SSL certificate served on the backend server's HTTPS port is issued to www.endoncambodia.com — not to neuralsh.com. Mail service certificates are issued to *.onesala.com. Any client connecting directly to the origin IP receives a certificate warning, indicating that certificate management has not been performed for this shared hosting environment.",
    "impact":"This finding confirms that infrastructure-level SSL hygiene has not been maintained and corroborates the shared hosting risk (N-004). It also discloses co-tenant domain names through certificate inspection.",
    "references":["https://owasp.org/Top10/A02_2021-Cryptographic_Failures/"],
    "remediation":"Issue a dedicated SSL certificate for the neuralsh.com domain at the origin server level. Ensure each hosted domain has its own certificate or that the server certificate covers all hosted domains as Subject Alternative Names (SANs).",
    "evidence":"Figure 4.8 — openssl output showing certificate issued to www.endoncambodia.com and *.onesala.com" },

  { "id":"N-009","severity":"Medium","cvss":"5.4","risk_rating":"Medium",
    "title":"CSP Allows unsafe-inline Scripts",
    "host":"neuralsh.com","tool":"curl",
    "likelihood":"Medium","status":"Confirmed",
    "description":"The Content-Security-Policy header on the main application includes 'unsafe-inline' in the script-src directive. This directive instructs the browser to allow execution of inline JavaScript, including dynamically injected script blocks and event handlers.",
    "impact":"If a Cross-Site Scripting (XSS) vulnerability is present in any part of the application, the CSP would not prevent exploitation of inline injection, rendering the entire Content Security Policy protection ineffective.",
    "references":["https://owasp.org/Top10/A03_2021-Injection/","https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"],
    "remediation":"Replace 'unsafe-inline' with per-request nonces ('nonce-{nonce}'). Nuxt.js has built-in CSP nonce support via its security plugin.",
    "evidence":"curl response headers confirming Content-Security-Policy: script-src 'self' 'unsafe-inline'" },

  { "id":"N-010","severity":"Medium","cvss":"4.3","risk_rating":"Medium",
    "title":"Wildcard DNS Configured",
    "host":"*.neuralsh.com","tool":"dig",
    "likelihood":"Low","status":"Confirmed",
    "description":"A wildcard DNS record is configured for *.neuralsh.com, causing any subdomain query to resolve to the origin IP 103.16.62.217. This means an attacker could use subdomains such as login.neuralsh.com or secure.neuralsh.com in phishing campaigns, and these domains would resolve to a real IP address.",
    "impact":"The wildcard DNS increases the credibility of phishing attacks by using legitimate subdomains of the target domain. Users are significantly more likely to trust a URL ending in .neuralsh.com than an arbitrary attacker-controlled domain.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
    "remediation":"Remove the wildcard DNS record from Cloudflare. Define only explicit A records for legitimate subdomains (mail.neuralsh.com, www.neuralsh.com).",
    "evidence":"Figure 4.7 — dig showing randomxyz123.neuralsh.com resolves to 103.16.62.217" },

  { "id":"N-016","severity":"Medium","cvss":"5.3","risk_rating":"Medium",
    "title":"Directory Listing Enabled on Apache",
    "host":"103.16.62.217","tool":"curl",
    "likelihood":"Low","status":"Confirmed",
    "description":"Apache's directory listing feature is enabled at the document root for the neuralsh.com virtual host. A direct HTTP request to the origin IP returns an 'Index of /' page, listing all files in the web root with their filenames and modification timestamps.",
    "impact":"Any deployed application files would be listed with full filenames and modification timestamps, providing direct reconnaissance information that accelerates targeted attacks and could expose backup files or configuration files.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
    "remediation":"Add 'Options -Indexes' to the Apache configuration or a .htaccess file in the document root to disable directory listing.",
    "evidence":"curl response showing 'Index of /' from direct HTTP request to 103.16.62.217" },

  { "id":"N-020","severity":"Medium","cvss":"6.1","risk_rating":"Medium",
    "title":"Shared Hosting Co-Tenant Identified: onesala.com",
    "host":"103.16.62.217","tool":"curl, openssl",
    "likelihood":"Medium","status":"Confirmed",
    "description":"HTTP redirects from ports 2077 and 2082 on the origin server explicitly redirect to www.onesala.com:2078 and www.onesala.com:2083, confirming onesala.com as a named, verifiable co-tenant on the same physical server as neuralsh.com. This was discovered during the follow-up scan on 10 June 2026.",
    "impact":"This finding elevates N-004 (Shared Hosting Lateral Movement Risk) from theoretical to confirmed with a real third-party victim identified. A breach of neuralsh.com's infrastructure now has documented third-party data protection implications.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
    "remediation":"No direct fix at the application level. Long-term remediation requires migration to isolated infrastructure. Short-term: immediately firewall WHM to prevent the co-tenancy risk from being exploited.",
    "evidence":"curl showing HTTP redirect from 103.16.62.217:2077 to www.onesala.com:2078" },

  { "id":"N-011","severity":"Low","cvss":"3.7","risk_rating":"Low",
    "title":"Information Disclosure via Error Messages",
    "host":"neuralsh.com/api/*","tool":"curl",
    "likelihood":"Low","status":"Confirmed",
    "description":"API error responses disclose internal details including the full request URL, internal status messages, parameter names expected by the endpoint, and backend framework identification strings. Example response: {\"error\":true,\"url\":\"https://neuralsh.com/api/geocode\",\"statusCode\":400,\"message\":\"Latitude and longitude are required\"}.",
    "impact":"Verbose error messages accelerate targeted attacks by reducing the reconnaissance effort required to map the API surface and understand expected parameter formats for each endpoint.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
    "remediation":"Return generic error responses to clients (e.g., '400 Bad Request'). Log detailed error information server-side only. Remove parameter names from all client-facing error messages.",
    "evidence":"curl to /api/geocode with missing parameters returning detailed internal error JSON" },

  { "id":"N-012","severity":"Low","cvss":"3.1","risk_rating":"Low",
    "title":"SPF Softfail / DMARC Quarantine",
    "host":"neuralsh.com DNS","tool":"dig",
    "likelihood":"Low","status":"Confirmed",
    "description":"The SPF record uses ~all (softfail) rather than -all (hardfail), and the DMARC policy is set to p=quarantine rather than p=reject. Emails from unauthorized senders spoofing @neuralsh.com addresses are flagged but not definitively rejected.",
    "impact":"Phishing emails using the neuralsh.com brand may be delivered to recipients whose mail servers do not strictly enforce SPF, enabling brand impersonation attacks with a degree of legitimacy.",
    "references":["https://dmarc.org/","https://tools.ietf.org/html/rfc7208"],
    "remediation":"Change SPF to: v=spf1 +mx +a +ip4:103.16.62.217 -all. Change DMARC to: v=DMARC1; p=reject; rua=mailto:dmarc@neuralsh.com.",
    "evidence":"Figure 4.6 — dig TXT output showing SPF ~all softfail and DMARC p=quarantine" },

  { "id":"N-017","severity":"Low","cvss":"3.1","risk_rating":"Low",
    "title":"cPanel Version Disclosure",
    "host":"103.16.62.217:2083","tool":"curl",
    "likelihood":"Low","status":"Confirmed",
    "description":"The cPanel version is disclosed via magic revision numbers embedded in static asset paths in the HTML source: cPanel_magic_revision_1698766296. This timestamp-based revision number can be cross-referenced to identify the exact cPanel version installed.",
    "impact":"Version disclosure enables targeted CVE lookup for that specific cPanel version, allowing an attacker to identify known unpatched vulnerabilities without conducting active version scanning.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
    "remediation":"Update cPanel to the latest stable version. Configure cPanel to suppress magic revision numbers in static asset paths.",
    "evidence":"curl to 103.16.62.217:2083 — HTML source contains cPanel_magic_revision_1698766296 in static asset paths" },

  { "id":"N-019","severity":"Low","cvss":"3.5","risk_rating":"Low",
    "title":"SMTP Port 25 Transitioned from Filtered to Open",
    "host":"103.16.62.217:25","tool":"Nmap, nc (follow-up scan 10 June 2026)",
    "likelihood":"Low","status":"Confirmed",
    "description":"Port 25 was listed as filtered in the June 6 baseline scan and open in the June 10 follow-up scan, accepting TCP connections. The unexplained transition indicates that a firewall rule was modified between the two scans without a documented change control process.",
    "impact":"An open SMTP port enables direct mail relay testing, SMTP user enumeration (VRFY, EXPN commands), and potential spam relay abuse if the Exim configuration allows unauthenticated relaying.",
    "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
    "remediation":"Investigate why the port 25 firewall rule was removed. If direct SMTP delivery is not required, restore the firewall block on port 25. Ensure Exim requires authentication for all outbound relay.",
    "evidence":"Comparison of June 6 Nmap baseline scan (25/tcp filtered) vs June 10 follow-up scan (25/tcp open)" },
]

# ── Screenshot/image path map ─────────────────────────────────────────────────
IMG_MAP = {
    "fig42":  ("fig42_ssh_kali.png",        SHOTS, "Figure 4.2: SSH connection to Kali Linux VM"),
    "fig43":  ("fig43_tools_verify.png",    SHOTS, "Figure 4.3: Tool version verification — Nmap, Nikto, Metasploit"),
    "fig44":  ("fig44_website.png",         SHOTS, "Figure 4.4: neuralsh.com homepage"),
    "fig45":  ("fig45_whois.png",           SHOTS, "Figure 4.5: WHOIS lookup for neuralsh.com"),
    "fig46":  ("fig46_dig_mx.png",          SHOTS, "Figure 4.6: dig MX and TXT records showing SPF and DMARC"),
    "fig47":  ("fig47_wildcard_dns.png",    SHOTS, "Figure 4.7: dig confirming wildcard DNS — randomxyz123.neuralsh.com resolves to origin IP"),
    "fig48":  ("fig48_ssl_cert.png",        SHOTS, "Figure 4.8: SSL certificate showing endoncambodia.com and onesala.com on same server"),
    "fig49":  ("fig49_nmap.png",            SHOTS, "Figure 4.9: Nmap scan of origin IP — 23 open ports"),
    "fig410": ("fig410_cpanel_whm.png",     SHOTS, "Figure 4.10: cPanel and WHM login pages accessible from public internet"),
    "fig411": ("fig411_mikrotik.png",       SHOTS, "Figure 4.11: MikroTik RouterOS curl response confirming WebFig"),
    "fig412": ("fig412_nikto.png",          SHOTS, "Figure 4.12: Nikto scan results"),
    "fig413": ("fig413_nuclei.png",         SHOTS, "Figure 4.13: Nuclei scan — 0 matches (WAF absorbing probes)"),
    "fig414": ("fig414_burp_waf.png",       SHOTS, "Figure 4.14: Burp Suite — cloudflare vs direct origin (WAF bypass confirmed)"),
    "fig415": ("fig415_ratelimit.png",      SHOTS, "Figure 4.15: Rate limit bypass — 50/50 tokens, 0 rate-limit responses"),
    "fig416": ("fig416_jwt_404.png",        SHOTS, "Figure 4.16: JWT endpoint curl — HTTP 200 confirmed live as of 11 June 2026"),
    "fig417": ("fig417_whm_browser.png",    SHOTS, "Figure 4.17: WHM admin panel accessible from public internet (103.16.62.217:2087)"),
    "fig418": ("fig418_mikrotik_browser.png",SHOTS,"Figure 4.18: MikroTik WebFig login — RouterOS v6.49.18, admin pre-filled"),
    "fig419": ("fig419_mysql_connect.png",  SHOTS, "Figure 4.19: MySQL connection from public IP — authentication prompt exposed"),
    "fig422": ("fig422_attack_chains.png",  SHOTS, "Figure 4.22: Attack chain diagram — 4 confirmed attack vectors"),
}

# ── Markdown → docx state machine ────────────────────────────────────────────
def process_md(doc):
    with open(MD, encoding='utf-8') as fh:
        lines = fh.readlines()

    in_code  = False
    code_buf = []
    in_table = False
    table_rows = []
    skip_finding_prose = False   # True once we hit ## 5.3, use cards instead

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip('\n')
        stripped = line.strip()

        # ── code block ─────────────────────────────────────────────────────
        if stripped.startswith('```'):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                code_block(doc, '\n'.join(code_buf))
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # ── horizontal rule ────────────────────────────────────────────────
        if stripped in ('---', '***', '___'):
            i += 1
            continue

        # ── table rows ─────────────────────────────────────────────────────
        if stripped.startswith('|') and stripped.endswith('|'):
            cols = [c.strip() for c in stripped[1:-1].split('|')]
            # skip separator rows
            if not all(re.fullmatch(r'-+:?|:?-+', c.replace(' ','')) for c in cols):
                table_rows.append(cols)
            in_table = True
            i += 1
            continue
        else:
            if in_table:
                if not skip_finding_prose:
                    md_table(doc, table_rows)
                table_rows = []
                in_table = False

        # ── image placeholder lines ─────────────────────────────────────────
        m_img = re.match(r'\*\[Figure (4\.\d+):[^\]]+\]\*', stripped)
        if m_img:
            key = 'fig4' + m_img.group(1).split('.')[1]
            if key in IMG_MAP:
                fn, folder, cap = IMG_MAP[key]
                add_img(doc, os.path.join(folder, fn), cap)
            i += 1
            continue

        # ── headings ───────────────────────────────────────────────────────
        if stripped.startswith('#### '):
            sec_head(doc, stripped[5:], level=3)
            i += 1; continue
        if stripped.startswith('### '):
            txt = stripped[4:]
            # detect 5.3 section to switch to card mode
            if re.match(r'^5\.3\b', txt):
                skip_finding_prose = True
                sec_head(doc, txt, level=1)
                doc.add_paragraph()
                # insert all finding cards here
                for f in FINDINGS:
                    finding_card(doc, f)
                # advance until end of 5.3 content
                while i < len(lines):
                    l = lines[i].strip()
                    # stop when we hit ## 5.4 or ##  6.
                    if re.match(r'^#{1,2}\s+5\.[4-9]', l) or re.match(r'^#{1,2}\s+6\.', l) or re.match(r'^#{1,2}\s+Chapter 6', l, re.I):
                        break
                    i += 1
                continue
            sec_head(doc, txt, level=2)
            i += 1; continue
        if stripped.startswith('## '):
            txt = stripped[3:]
            # map known chapter markers
            ch_map = {
                'Declaration': None,
                'Abstract': None,
                'Table of Contents': None,
            }
            if any(txt.startswith(k) for k in ['4.1','4.2','4.3','4.4','4.5','4.6','4.7','4.8']):
                sec_head(doc, txt, level=1)
            elif any(txt.startswith(k) for k in ['5.1','5.2','5.3','5.4','5.5','5.6']):
                sec_head(doc, txt, level=1)
            elif re.match(r'^\d+\.', txt):
                sec_head(doc, txt, level=1)
            else:
                sec_head(doc, txt, level=1)
            i += 1; continue
        if stripped.startswith('# '):
            ch_head(doc, stripped[2:])
            i += 1; continue

        # ── bullet lists ───────────────────────────────────────────────────
        m_bullet = re.match(r'^[-*]\s+(.+)', stripped)
        if m_bullet:
            if not skip_finding_prose:
                p = doc.add_paragraph(style='List Bullet')
                p.paragraph_format.left_indent = Cm(1.27)
                p.paragraph_format.first_line_indent = Cm(0)
                r = p.add_run(m_bullet.group(1))
                fmt(r, size=12)
            i += 1; continue

        # ── blank line ──────────────────────────────────────────────────────
        if not stripped:
            i += 1; continue

        # ── finding detail prose — skip after 5.3 triggered ───────────────
        if skip_finding_prose and re.match(r'^\*\*N-\d+', stripped):
            i += 1; continue

        # ── normal paragraph ───────────────────────────────────────────────
        # strip markdown bold/italic but keep text
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', stripped)
        clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
        clean = re.sub(r'`([^`]+)`', r'\1', clean)
        # skip pure metadata lines
        if clean.startswith('**Student:**') or clean.startswith('**Student ID:**'):
            i += 1; continue
        if not skip_finding_prose:
            body(doc, clean)
        i += 1

# ── Chapter title pages ───────────────────────────────────────────────────────
CHAPTER_TITLES = {
    'chapter_4': 'CHAPTER IV: IMPLEMENTATION AND DEPLOYMENT',
    'chapter_5': 'CHAPTER V: RESULTS, ANALYSIS AND REMEDIATION',
}

def build_doc():
    doc = new_doc()

    # Title page
    ch_head(doc, 'VULNERABILITY ASSESSMENT AND PENETRATION TESTING (VAPT)\nON A WEB APPLICATION')
    body(doc, 'A Case Study of neuralsh.com', align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, bold=True)
    doc.add_paragraph()
    body(doc, 'Submitted in partial fulfilment of the requirements for the degree of\nBachelor of Science in Information Technology', align=WD_ALIGN_PARAGRAPH.CENTER, indent=0)
    doc.add_paragraph()
    body(doc, 'Institution of Technology of Cambodia', align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, bold=True)
    body(doc, 'June 2026', align=WD_ALIGN_PARAGRAPH.CENTER, indent=0)

    # Process full markdown
    process_md(doc)

    doc.save(OUT)
    print(f"Saved: {OUT}")

if __name__ == '__main__':
    build_doc()
