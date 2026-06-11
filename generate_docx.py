#!/usr/bin/env python3
"""
generate_docx.py — VAPT Thesis → ITC-compliant Word Document
ITC Format (from Report Writing Format guidelines):
  Margins: Left 3cm, Right 2cm, Top 2cm, Bottom 2cm
  Font: Times New Roman only
  Headings: Chapter=16pt bold ALL CAPS centered | X.X=14pt bold | X.X.X=12pt bold
  Body: 12pt, 1.5 line spacing, 6pt after paragraph, justified
  TOC: auto-generated via Word field (press Ctrl+A then F9 in Word to update)
  Page numbers: Roman numerals for front matter, Arabic from Chapter I

Requirements: pip install python-docx
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

# ── Color palette ─────────────────────────────────────────────────────────────
C = {
    "critical": ("8B0000", "FFFFFF"),
    "high":     ("C00000", "FFFFFF"),
    "medium":   ("FFC000", "000000"),
    "low":      ("70AD47", "FFFFFF"),
    "label":    ("D9D9D9", "000000"),
    "blue":     ("2E74B5", "FFFFFF"),
}
def hex2rgb(h): return RGBColor(int(h[:2],16), int(h[2:4],16), int(h[4:],16))

# ── XML helpers ───────────────────────────────────────────────────────────────
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
    v = OxmlElement('w:vAlign')
    v.set(qn('w:val'), val)
    tcPr.append(v)

def add_page_number(doc, numeral_format='decimal'):
    """Add page number footer (decimal or upperRoman)."""
    section = doc.sections[-1]
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.clear()
    run = p.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.extend([fldChar1, instrText, fldChar2, fldChar3])
    # Set number format on section
    sectPr = section._sectPr
    pgNumType = sectPr.find(qn('w:pgNumType'))
    if pgNumType is None:
        pgNumType = OxmlElement('w:pgNumType')
        sectPr.append(pgNumType)
    pgNumType.set(qn('w:fmt'), numeral_format)
    if numeral_format == 'upperRoman':
        pgNumType.set(qn('w:start'), '1')

def add_section_break(doc, restart_arabic=False):
    """Add a section break (next page) for switching page number format."""
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    sectPr = OxmlElement('w:sectPr')
    pgSz = OxmlElement('w:pgSz')
    pgSz.set(qn('w:w'), str(int(21.0 / 2.54 * 1440)))
    pgSz.set(qn('w:h'), str(int(29.7 / 2.54 * 1440)))
    pgMar = OxmlElement('w:pgMar')
    pgMar.set(qn('w:top'),    str(int(2.0 / 2.54 * 1440)))
    pgMar.set(qn('w:right'),  str(int(2.0 / 2.54 * 1440)))
    pgMar.set(qn('w:bottom'), str(int(2.0 / 2.54 * 1440)))
    pgMar.set(qn('w:left'),   str(int(3.0 / 2.54 * 1440)))
    sectPr.append(pgSz)
    sectPr.append(pgMar)
    if restart_arabic:
        pgNumType = OxmlElement('w:pgNumType')
        pgNumType.set(qn('w:fmt'), 'decimal')
        pgNumType.set(qn('w:start'), '1')
        sectPr.append(pgNumType)
    pPr.append(sectPr)

def add_toc_field(doc):
    """Insert a TOC field that Word will populate on Ctrl+A, F9."""
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run()
    # begin
    fc1 = OxmlElement('w:fldChar')
    fc1.set(qn('w:fldCharType'), 'begin')
    run._r.append(fc1)
    # instruction
    it = OxmlElement('w:instrText')
    it.set(qn('xml:space'), 'preserve')
    it.text = ' TOC \\o "1-3" \\h \\z \\u '
    run._r.append(it)
    # separate
    fc2 = OxmlElement('w:fldChar')
    fc2.set(qn('w:fldCharType'), 'separate')
    run._r.append(fc2)
    # placeholder text
    p2 = doc.add_paragraph()
    p2.paragraph_format.first_line_indent = Cm(0)
    r2 = p2.add_run('[Right-click here and select "Update Field" to generate Table of Contents]')
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    # end
    run2 = p2.add_run()
    fc3 = OxmlElement('w:fldChar')
    fc3.set(qn('w:fldCharType'), 'end')
    run2._r.append(fc3)

# ── Document setup ────────────────────────────────────────────────────────────
def new_doc():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width    = Cm(21.0)
    sec.page_height   = Cm(29.7)
    sec.left_margin   = Cm(3.0)   # ITC: 3cm left
    sec.right_margin  = Cm(2.0)   # ITC: 2cm right
    sec.top_margin    = Cm(2.0)   # ITC: 2cm top
    sec.bottom_margin = Cm(2.0)   # ITC: 2cm bottom

    # Configure heading styles
    _setup_heading_styles(doc)

    # Normal body style
    n = doc.styles['Normal']
    n.font.name = 'Times New Roman'
    n.font.size = Pt(12)
    n.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    n.paragraph_format.space_after = Pt(6)
    return doc

def _setup_heading_styles(doc):
    """ITC heading hierarchy: Chapter=16pt ALL CAPS | X.X=14pt | X.X.X=12pt"""
    defs = [
        ('Heading 1', 16, True,  WD_ALIGN_PARAGRAPH.CENTER, True,  Pt(24), Pt(12)),
        ('Heading 2', 14, True,  WD_ALIGN_PARAGRAPH.LEFT,   False, Pt(12), Pt(6)),
        ('Heading 3', 12, True,  WD_ALIGN_PARAGRAPH.LEFT,   False, Pt(8),  Pt(4)),
        ('Heading 4', 12, False, WD_ALIGN_PARAGRAPH.LEFT,   False, Pt(6),  Pt(3)),
    ]
    for name, size, bold, align, page_break, sb, sa in defs:
        try:
            s = doc.styles[name]
            s.font.name = 'Times New Roman'
            s.font.size = Pt(size)
            s.font.bold = bold
            s.font.color.rgb = RGBColor(0, 0, 0)
            s.paragraph_format.alignment = align
            s.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
            s.paragraph_format.space_before = sb
            s.paragraph_format.space_after = sa
            s.paragraph_format.first_line_indent = Cm(0)
            if page_break:
                s.paragraph_format.page_break_before = True
        except Exception:
            pass

# ── Typography helpers ────────────────────────────────────────────────────────
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
    """Chapter heading — Heading 1 style: 16pt bold ALL CAPS centered, page break"""
    p = doc.add_paragraph(style='Heading 1')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text.upper())
    fmt(run, size=16, bold=True)

def sec_head(doc, text, level=1):
    """Section heading: level1=14pt bold, level2=12pt bold, level3=12pt bold"""
    style = {1: 'Heading 2', 2: 'Heading 3', 3: 'Heading 4'}.get(level, 'Heading 3')
    size  = {1: 14, 2: 12, 3: 12}.get(level, 12)
    p = doc.add_paragraph(style=style)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    fmt(run, size=size, bold=True)

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
    ncols = max(len(r) for r in rows_data)
    tbl = doc.add_table(rows=len(rows_data), cols=ncols)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row in enumerate(rows_data):
        for ci in range(ncols):
            cell_txt = row[ci] if ci < len(row) else ''
            cell = tbl.cell(ri, ci)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            r = p.add_run(cell_txt.strip())
            fmt(r, size=11, bold=(ri == 0))
            if ri == 0:
                set_bg(cell, C['blue'][0])
                r.font.color.rgb = hex2rgb(C['blue'][1])
            # severity color cells
            lower = cell_txt.strip().lower()
            if lower in ('critical',):
                set_bg(cell, C['critical'][0])
                r.font.color.rgb = hex2rgb(C['critical'][1])
                r.font.bold = True
            elif lower in ('high',):
                set_bg(cell, C['high'][0])
                r.font.color.rgb = hex2rgb(C['high'][1])
                r.font.bold = True
            elif lower in ('medium',):
                set_bg(cell, C['medium'][0])
                r.font.bold = True
            elif lower in ('low',):
                set_bg(cell, C['low'][0])
                r.font.color.rgb = hex2rgb(C['low'][1])
                r.font.bold = True
    doc.add_paragraph()

# ── Finding Card (SE_LYTHENG style) ──────────────────────────────────────────
def finding_card(doc, f):
    sev = f['severity'].lower()
    fill, txt = C[sev]

    sec_head(doc, f"{f['id']} — {f['title']}", level=2)

    # 3-column table: label(3.4cm) | left-value(5.8cm) | right-value(5.8cm)
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
    p0.paragraph_format.first_line_indent = Cm(0)
    r0 = p0.add_run(badge)
    fmt(r0, size=11, bold=True, color=txt)
    set_bg(c0, fill)
    set_cell_vert(c0)

    def lv(ri, lbl, val):
        """Standard label | merged-value row"""
        lc = tbl.cell(ri, 0)
        vc = tbl.cell(ri, 1)
        vc.merge(tbl.cell(ri, 2))
        set_bg(lc, C['label'][0])
        set_cell_vert(lc)
        lc.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        vc.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        fmt(lc.paragraphs[0].add_run(lbl), size=11, bold=True)
        fmt(vc.paragraphs[0].add_run(val), size=11)

    def ll(ri, lbl, items):
        """Label | merged-value with numbered list"""
        lc = tbl.cell(ri, 0)
        vc = tbl.cell(ri, 1)
        vc.merge(tbl.cell(ri, 2))
        set_bg(lc, C['label'][0])
        set_cell_vert(lc)
        lc.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        fmt(lc.paragraphs[0].add_run(lbl), size=11, bold=True)
        for i, item in enumerate(items):
            p_ = vc.paragraphs[0] if i == 0 else vc.add_paragraph()
            p_.paragraph_format.first_line_indent = Cm(0)
            fmt(p_.add_run(f"{i+1}.  {item}"), size=11)

    lv(1, "Description:", f['description'])

    # Row 2 — Risks: two colored cells side by side
    lc2 = tbl.cell(2, 0)
    lk  = tbl.cell(2, 1)
    rk  = tbl.cell(2, 2)
    set_bg(lc2, C['label'][0])
    set_cell_vert(lc2)
    lc2.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
    fmt(lc2.paragraphs[0].add_run("Risks:"), size=11, bold=True)
    # Likelihood cell
    lsev = f['likelihood'].lower()
    lf, lt = C.get(lsev, C['medium'])
    set_bg(lk, lf)
    set_cell_vert(lk)
    plk = lk.paragraphs[0]
    plk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    plk.paragraph_format.first_line_indent = Cm(0)
    fmt(plk.add_run(f"Likelihood: {f['likelihood']}"), size=11, bold=True, color=lt)
    # Risk Rating cell
    set_bg(rk, fill)
    set_cell_vert(rk)
    prk = rk.paragraphs[0]
    prk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    prk.paragraph_format.first_line_indent = Cm(0)
    fmt(prk.add_run(f"Risk Rating: {f['risk_rating']}"), size=11, bold=True, color=txt)

    lv(3, "Impact:",      f['impact'])
    lv(4, "Tool Used:",   f['tool'])
    ll(5, "References:",  f['references'])
    lv(6, "Remediation:", f['remediation'])
    lv(7, "Evidence:",    f['evidence'])

    doc.add_paragraph()

# ── All 20 findings ───────────────────────────────────────────────────────────
FINDINGS = [
  {"id":"N-001","severity":"Critical","cvss":"9.8","risk_rating":"Critical",
   "title":"MySQL Port 3306 Exposed to Internet",
   "host":"103.16.62.217:3306","tool":"Nmap, mysql-client",
   "likelihood":"High","status":"Confirmed",
   "description":"The MySQL 8.0.43 database server is directly accessible from the public internet on port 3306, accepting full TCP connections from any external IP address. An attacker does not need to compromise the web application to reach the database — authentication can be attempted directly at the database layer, bypassing all application-level access controls. No rate limiting or IP-based blocking exists at the database layer.",
   "impact":"Successful access grants full read and write access to all application databases, potentially including user records, session data, and API secrets. MySQL's User Defined Function (UDF) feature could further be abused to achieve remote command execution on the server.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-2122"],
   "remediation":"Restrict port 3306 to localhost or a trusted management VPN via firewall rules. Database ports must never be exposed to the public internet.",
   "evidence":"Figure 4.9 — Nmap scan confirming 3306/tcp open mysql MySQL 8.0.43; Figure 4.19 — MySQL connection accepted from public IP"},

  {"id":"N-002","severity":"Critical","cvss":"9.1","risk_rating":"Critical",
   "title":"MikroTik Admin Panel Exposed (Port 9001)",
   "host":"103.16.62.217:9001","tool":"Nmap, curl, browser",
   "likelihood":"High","status":"Confirmed",
   "description":"The MikroTik RouterOS web configuration interface (WebFig) is publicly accessible on port 9001, returning HTTP 200 with a fully rendered login page. The login form pre-fills 'admin' as the default username. MikroTik devices ship with a factory default of admin/blank password — if this default has not been changed, full network device control is available without any credential knowledge.",
   "impact":"An attacker with RouterOS access can modify routing tables, capture all network traffic, create persistent backdoor accounts, remove firewall rules, and disrupt all hosted services on the server.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://nvd.nist.gov/vuln/detail/CVE-2018-14847"],
   "remediation":"Restrict port 9001 to a trusted management IP via firewall. Change MikroTik default credentials immediately. Disable unused RouterOS services.",
   "evidence":"Figure 4.11 — curl response confirming RouterOS WebFig; Figure 4.18 — Browser showing MikroTik WebFig login with admin pre-filled, RouterOS v6.49.18"},

  {"id":"N-013","severity":"Critical","cvss":"9.8","risk_rating":"Critical",
   "title":"cPanel Admin Panel Exposed (Port 2083)",
   "host":"103.16.62.217:2083","tool":"Nmap, curl",
   "likelihood":"High","status":"Confirmed",
   "description":"The cPanel web hosting control panel is publicly accessible on port 2083 with no IP restriction and no two-factor authentication prompt. cPanel provides full management of the hosting account: file manager, database administration via phpMyAdmin, email account control, FTP credential creation, and subdomain configuration.",
   "impact":"An attacker who compromises the registered email account can use the password reset link to gain full hosting account access without brute force. All application files and databases then become accessible.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://docs.cpanel.net/cpanel/security/two-factor-authentication-for-cpanel/"],
   "remediation":"Restrict port 2083 to trusted management IPs via Cloudways firewall. Enable two-factor authentication on cPanel immediately.",
   "evidence":"Figure 4.10 — curl response showing cPanel Login title confirming public accessibility"},

  {"id":"N-014","severity":"Critical","cvss":"10.0","risk_rating":"Critical",
   "title":"WHM Root Panel Exposed (Port 2087)",
   "host":"103.16.62.217:2087","tool":"Nmap, curl, browser",
   "likelihood":"High","status":"Confirmed",
   "description":"WHM (Web Host Manager) is the root-level server administration panel for cPanel-based servers. It is publicly accessible on port 2087 with no IP restriction, no two-factor authentication, and no account lockout. WHM access is functionally equivalent to root shell access: it provides a built-in Terminal, full server configuration control, and administrative access to every hosted account on the server.",
   "impact":"An attacker who gains WHM access compromises not only neuralsh.com but every other hosted domain on the shared server simultaneously. This is the highest-severity finding in the engagement (CVSS 10.0 — maximum score).",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://docs.cpanel.net/whm/security-center/"],
   "remediation":"Immediately firewall port 2087 to trusted IPs only. This single action eliminates the highest-risk vector in the engagement.",
   "evidence":"Figure 4.17 — Browser showing WHM login page at 103.16.62.217:2087 with SSL warning (no authentication bypass required)"},

  {"id":"N-003","severity":"High","cvss":"7.2","risk_rating":"High",
   "title":"SSH Port 22 Publicly Accessible",
   "host":"103.16.62.217:22","tool":"Nmap, ssh",
   "likelihood":"Medium","status":"Confirmed",
   "description":"OpenSSH 8.9p1 is publicly accessible on port 22. SSH key-based authentication was confirmed as the enforced method for tested usernames, which reduces the immediate exploitation risk. However, the port remains exposed to brute-force attempts for any account that may have password authentication enabled.",
   "impact":"The SMTP banner confirms this is a cPanel shared hosting server where the primary user typically holds sudo privileges. Successful SSH compromise is therefore equivalent to root access to the entire server.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://www.cisecurity.org/benchmark/ubuntu_linux"],
   "remediation":"Enforce PasswordAuthentication no in /etc/ssh/sshd_config. Install fail2ban with aggressive thresholds. Restrict SSH to a trusted management IP via firewall.",
   "evidence":"Figure 4.9 — Nmap scan confirming 22/tcp open OpenSSH 8.9p1"},

  {"id":"N-004","severity":"High","cvss":"7.5","risk_rating":"High",
   "title":"Shared Hosting Lateral Movement Risk",
   "host":"103.16.62.217 (shared infrastructure)","tool":"openssl, curl",
   "likelihood":"Medium","status":"Confirmed",
   "description":"The origin server is a shared cPanel hosting environment (Cloudways/cprapid.com) hosting multiple clients on the same physical server. SSL certificates issued to *.onesala.com and www.endoncambodia.com confirmed the presence of other tenants. On shared cPanel hosting, a single WHM-level compromise grants access to the files, databases, and email of every co-hosted account simultaneously.",
   "impact":"A compromise of neuralsh.com's hosting account constitutes a data breach affecting organizations with no relationship to neuralsh.com and no awareness of its security posture, creating third-party data protection liability.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://cheatsheetseries.owasp.org/cheatsheets/Infrastructure_as_Code_Security_Cheat_Sheet.html"],
   "remediation":"Migrate neuralsh.com to a dedicated server or isolated cloud instance. Short-term: firewall WHM immediately to eliminate the most direct lateral movement path.",
   "evidence":"Figure 4.8 — SSL certificate showing onesala.com and endoncambodia.com on the same origin server"},

  {"id":"N-005","severity":"High","cvss":"9.1","risk_rating":"High",
   "title":"Rate Limit Bypass via X-Forwarded-For Header Spoofing",
   "host":"neuralsh.com/web/v1/init/token","tool":"Burp Suite, curl, Python script",
   "likelihood":"High","status":"Exploited",
   "description":"The application's rate-limiting mechanism uses the client-supplied X-Forwarded-For header as the identifier for tracking request rates per IP address. Because X-Forwarded-For is fully controllable by the client, an attacker can supply a different random IP value on each request, making every request appear to originate from a unique source and bypassing the rate limit entirely.",
   "impact":"Exploitation confirmed at 100% success rate: fifty consecutive requests with rotating X-Forwarded-For values all received HTTP 200 responses — zero rate-limit responses returned. This bypass enables unlimited JWT token farming and applies to any endpoint using the same IP-tracking logic. STATUS: CONFIRMED EXPLOITED.",
   "references":["https://owasp.org/Top10/A04_2021-Insecure_Design/","https://developers.cloudflare.com/fundamentals/reference/http-headers/"],
   "remediation":"Replace X-Forwarded-For with Cloudflare's CF-Connecting-IP header for all rate-limiting logic. CF-Connecting-IP is set by Cloudflare and cannot be spoofed by the client.",
   "evidence":"Figure 4.15 — Burp Suite Intruder showing fifty/fifty requests returning HTTP 200 with rotating X-Forwarded-For headers; zero rate-limit responses"},

  {"id":"N-015","severity":"High","cvss":"7.5","risk_rating":"High",
   "title":"Webmail Interface Exposed (Port 2096)",
   "host":"103.16.62.217:2096","tool":"Nmap, curl",
   "likelihood":"Medium","status":"Confirmed",
   "description":"The cPanel Webmail login interface is publicly accessible on port 2096 without IP restriction. This interface allows brute-force attacks against all email accounts hosted on the server, including @neuralsh.com addresses.",
   "impact":"A compromised email account can be used to trigger password reset flows for other services (cPanel, application accounts) and to send phishing emails from a legitimate @neuralsh.com address with valid DKIM signatures.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/","https://docs.cpanel.net/cpanel/email/webmail/"],
   "remediation":"Restrict port 2096 to trusted IPs via firewall. Enforce strong passwords on all email accounts. Implement CAPTCHA or account lockout on the webmail login.",
   "evidence":"Nmap scan — 2096/tcp open confirming cPanel Webmail public accessibility"},

  {"id":"N-018","severity":"High","cvss":"7.5","risk_rating":"High",
   "title":"Additional cPanel Interfaces Exposed (Ports 2078, 2091)",
   "host":"103.16.62.217:2078, 2091","tool":"Nmap, curl (follow-up scan, ten June 2026)",
   "likelihood":"Medium","status":"Confirmed",
   "description":"Ports 2078 and 2091 were not present in the June six baseline scan but appeared open in the June ten follow-up scan, both returning HTTP 401 with WWW-Authenticate: Basic realm=Restricted Area. These are additional cPanel management service ports whose appearance indicates infrastructure changes are being made without a security review.",
   "impact":"These ports represent additional credential brute-force attack surface for server management interfaces. The appearance of new open ports between scans also confirms absence of a change management process.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
   "remediation":"Restrict ports 2078 and 2091 via firewall. Conduct a full port audit of 103.16.62.217 and close all ports without a documented business purpose.",
   "evidence":"Follow-up Nmap scan (ten June 2026) — 2078/tcp and 2091/tcp open returning HTTP 401"},

  {"id":"N-006","severity":"Medium","cvss":"5.3","risk_rating":"Medium",
   "title":"API Routes Exposed in Client-Side JavaScript",
   "host":"neuralsh.com/_nuxt/","tool":"curl, grep",
   "likelihood":"Low","status":"Confirmed",
   "description":"The complete API route structure of the application is disclosed in the compiled Nuxt.js JavaScript bundle. Routes including /web/v1/init/token, /web/v1/text/search, /web/v1/image/search, /web/v1/report/save, and /api/geocode were extracted directly from the bundle without authentication or directory scanning.",
   "impact":"This reconnaissance eliminated the need for directory brute force and directly enabled the targeted exploitation of the unauthenticated token endpoint (N-007). Every internal API endpoint is effectively public knowledge.",
   "references":["https://owasp.org/Top10/A01_2021-Broken_Access_Control/"],
   "remediation":"Minimize unnecessary route exposure in the bundle. Implement an API gateway with strict allowlisting. Secure all API endpoints with proper authentication regardless of whether they appear in client code.",
   "evidence":"curl extraction of API routes from /_nuxt/Bpuv52g-.js bundle"},

  {"id":"N-007","severity":"Medium","cvss":"5.3","risk_rating":"Medium",
   "title":"Unauthenticated JWT Token Issuance",
   "host":"neuralsh.com/web/v1/init/token","tool":"curl, CyberChef, hashcat, Burp Suite",
   "likelihood":"High","status":"Exploited",
   "description":"The token endpoint issues a valid signed JWT token to any unauthenticated caller with no credentials, API key, device fingerprint, or identifying information required. Tokens carry a type:guest claim and a 30-minute validity window. A follow-up verification on eleven June 2026 confirmed the endpoint remains live and returning HTTP 200 — no remediation had been applied.",
   "impact":"Using the rate-limit bypass from N-005, fifty valid tokens were farmed in approximately three seconds. Each token granted real API access to search and category endpoints. JWT secret brute-force against rockyou.txt (14,344,391 candidates) was unsuccessful; however, token farming impact is independent of secret strength. STATUS: CONFIRMED EXPLOITED.",
   "references":["https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/","https://portswigger.net/web-security/jwt"],
   "remediation":"Require a browser-computed fingerprint, Cloudflare Turnstile challenge, or origin header validation before issuing tokens. Implement token binding to prevent reuse outside the originating browser session.",
   "evidence":"Figure 4.15 — fifty tokens collected; Figure 4.16 — endpoint confirmed live (HTTP 200) as of eleven June 2026"},

  {"id":"N-008","severity":"Medium","cvss":"5.9","risk_rating":"Medium",
   "title":"SSL Certificate Mismatch on Backend Server",
   "host":"103.16.62.217:443, 110, 143, 465","tool":"openssl",
   "likelihood":"Low","status":"Confirmed",
   "description":"The SSL certificate served on the backend server's HTTPS port is issued to www.endoncambodia.com — not to neuralsh.com. Mail service certificates are issued to *.onesala.com. Any client connecting directly to the origin IP receives a certificate warning, indicating that certificate management has not been performed for this shared hosting environment.",
   "impact":"This finding confirms that infrastructure-level SSL hygiene has not been maintained and corroborates the shared hosting risk (N-004). It also inadvertently discloses co-tenant domain names through certificate inspection.",
   "references":["https://owasp.org/Top10/A02_2021-Cryptographic_Failures/"],
   "remediation":"Issue a dedicated SSL certificate for the neuralsh.com domain at the origin server level. Ensure each hosted domain has its own certificate, or use a multi-SAN certificate covering all hosted domains.",
   "evidence":"Figure 4.8 — openssl output showing certificate issued to www.endoncambodia.com and *.onesala.com"},

  {"id":"N-009","severity":"Medium","cvss":"5.4","risk_rating":"Medium",
   "title":"CSP Allows unsafe-inline Scripts",
   "host":"neuralsh.com","tool":"curl",
   "likelihood":"Medium","status":"Confirmed",
   "description":"The Content-Security-Policy header on the main application includes 'unsafe-inline' in the script-src directive. This directive instructs the browser to allow execution of inline JavaScript, including dynamically injected script blocks and event handlers.",
   "impact":"If a Cross-Site Scripting vulnerability is present anywhere in the application, the CSP would not prevent exploitation of inline injection, rendering the entire Content Security Policy protection ineffective.",
   "references":["https://owasp.org/Top10/A03_2021-Injection/","https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"],
   "remediation":"Replace 'unsafe-inline' with per-request nonces ('nonce-{nonce}'). Nuxt.js has built-in CSP nonce support via its security plugin.",
   "evidence":"curl response headers confirming Content-Security-Policy: script-src 'self' 'unsafe-inline'"},

  {"id":"N-010","severity":"Medium","cvss":"4.3","risk_rating":"Medium",
   "title":"Wildcard DNS Configured",
   "host":"*.neuralsh.com","tool":"dig",
   "likelihood":"Low","status":"Confirmed",
   "description":"A wildcard DNS record is configured for *.neuralsh.com, causing any subdomain query to resolve to the origin IP 103.16.62.217. An attacker could use subdomains such as login.neuralsh.com or secure.neuralsh.com in phishing campaigns, and these domains would resolve to a real IP address.",
   "impact":"The wildcard DNS increases the credibility of phishing attacks. Users are significantly more likely to trust a URL ending in .neuralsh.com than an attacker-controlled domain.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
   "remediation":"Remove the wildcard DNS record from Cloudflare. Define only explicit A records for legitimate subdomains (mail.neuralsh.com, www.neuralsh.com).",
   "evidence":"Figure 4.7 — dig showing randomxyz123.neuralsh.com resolves to 103.16.62.217"},

  {"id":"N-016","severity":"Medium","cvss":"5.3","risk_rating":"Medium",
   "title":"Directory Listing Enabled on Apache",
   "host":"103.16.62.217","tool":"curl",
   "likelihood":"Low","status":"Confirmed",
   "description":"Apache's directory listing feature is enabled at the document root for the neuralsh.com virtual host. A direct HTTP request to the origin IP returns an 'Index of /' page, listing all files in the web root with their filenames and modification timestamps.",
   "impact":"Any deployed application files would be listed with full filenames and modification timestamps, providing direct reconnaissance information and potentially exposing backup files or configuration files.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
   "remediation":"Add 'Options -Indexes' to the Apache configuration or a .htaccess file in the document root to disable directory listing.",
   "evidence":"curl response showing 'Index of /' from direct HTTP request to 103.16.62.217"},

  {"id":"N-020","severity":"Medium","cvss":"6.1","risk_rating":"Medium",
   "title":"Shared Hosting Co-Tenant Identified: onesala.com",
   "host":"103.16.62.217","tool":"curl, openssl",
   "likelihood":"Medium","status":"Confirmed",
   "description":"HTTP redirects from ports 2077 and 2082 on the origin server explicitly redirect to www.onesala.com:2078 and www.onesala.com:2083, confirming onesala.com as a named, verifiable co-tenant on the same physical server as neuralsh.com. This was discovered during the follow-up scan on ten June 2026.",
   "impact":"This finding elevates N-004 (Shared Hosting Lateral Movement Risk) from theoretical to confirmed with a real third-party victim identified. A breach of neuralsh.com's infrastructure now carries documented third-party data protection implications.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
   "remediation":"No direct fix at the application level. Long-term remediation requires migration to isolated infrastructure. Short-term: firewall WHM immediately.",
   "evidence":"curl showing HTTP redirect from 103.16.62.217:2077 to www.onesala.com:2078"},

  {"id":"N-011","severity":"Low","cvss":"3.7","risk_rating":"Low",
   "title":"Information Disclosure via Error Messages",
   "host":"neuralsh.com/api/*","tool":"curl",
   "likelihood":"Low","status":"Confirmed",
   "description":"API error responses disclose internal details including the full request URL, internal status messages, parameter names expected by the endpoint, and backend framework identification strings. Example: {\"error\":true,\"url\":\"https://neuralsh.com/api/geocode\",\"statusCode\":400,\"message\":\"Latitude and longitude are required\"}.",
   "impact":"Verbose error messages reduce the reconnaissance effort required to map the API surface and understand expected parameter formats, accelerating targeted attacks.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
   "remediation":"Return generic error responses to clients. Log detailed error information server-side only. Remove parameter names from all client-facing error messages.",
   "evidence":"curl to /api/geocode with missing parameters returning detailed internal error JSON"},

  {"id":"N-012","severity":"Low","cvss":"3.1","risk_rating":"Low",
   "title":"SPF Softfail / DMARC Quarantine",
   "host":"neuralsh.com DNS","tool":"dig",
   "likelihood":"Low","status":"Confirmed",
   "description":"The SPF record uses ~all (softfail) rather than -all (hardfail), and the DMARC policy is set to p=quarantine rather than p=reject. Emails from unauthorized senders spoofing @neuralsh.com addresses are flagged but not definitively rejected.",
   "impact":"Phishing emails using the neuralsh.com brand may be delivered to recipients whose mail servers do not strictly enforce SPF, enabling brand impersonation attacks.",
   "references":["https://dmarc.org/","https://tools.ietf.org/html/rfc7208"],
   "remediation":"Change SPF to: v=spf1 +mx +a +ip4:103.16.62.217 -all. Change DMARC to: v=DMARC1; p=reject; rua=mailto:dmarc@neuralsh.com.",
   "evidence":"Figure 4.6 — dig TXT output showing SPF ~all softfail and DMARC p=quarantine"},

  {"id":"N-017","severity":"Low","cvss":"3.1","risk_rating":"Low",
   "title":"cPanel Version Disclosure",
   "host":"103.16.62.217:2083","tool":"curl",
   "likelihood":"Low","status":"Confirmed",
   "description":"The cPanel version is disclosed via magic revision numbers embedded in static asset paths in the HTML source: cPanel_magic_revision_1698766296. This timestamp-based revision number can be cross-referenced to identify the exact cPanel version installed.",
   "impact":"Version disclosure enables targeted CVE lookup for that specific cPanel version, allowing an attacker to identify known unpatched vulnerabilities without active version scanning.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
   "remediation":"Update cPanel to the latest stable version. Configure cPanel to suppress magic revision numbers in static asset paths.",
   "evidence":"curl to 103.16.62.217:2083 — HTML source contains cPanel_magic_revision_1698766296 in static asset paths"},

  {"id":"N-019","severity":"Low","cvss":"3.5","risk_rating":"Low",
   "title":"SMTP Port 25 Transitioned from Filtered to Open",
   "host":"103.16.62.217:25","tool":"Nmap, nc (follow-up scan, ten June 2026)",
   "likelihood":"Low","status":"Confirmed",
   "description":"Port 25 was listed as filtered in the June six baseline scan and open in the June ten follow-up scan, accepting TCP connections. The unexplained transition indicates that a firewall rule was modified between the two scans without a documented change control process.",
   "impact":"An open SMTP port enables direct mail relay testing, SMTP user enumeration (VRFY/EXPN commands), and potential spam relay abuse if the Exim configuration allows unauthenticated relaying.",
   "references":["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
   "remediation":"Investigate why the port twenty-five firewall rule was removed. If direct SMTP delivery is not required, restore the firewall block on port twenty-five.",
   "evidence":"Comparison of June six Nmap baseline (25/tcp filtered) vs June ten follow-up (25/tcp open)"},
]

# ── Screenshot map ─────────────────────────────────────────────────────────────
IMG_MAP = {
    "4.2":  (os.path.join(SHOTS,"fig42_ssh_kali.png"),         "Figure 4.2: SSH connection to Kali Linux VM"),
    "4.3":  (os.path.join(SHOTS,"fig43_tools_verify.png"),     "Figure 4.3: Tool version verification — Nmap, Nikto, Metasploit"),
    "4.4":  (os.path.join(SHOTS,"fig44_website.png"),          "Figure 4.4: neuralsh.com homepage"),
    "4.5":  (os.path.join(SHOTS,"fig45_whois.png"),            "Figure 4.5: WHOIS lookup for neuralsh.com"),
    "4.6":  (os.path.join(SHOTS,"fig46_dig_mx.png"),           "Figure 4.6: dig MX and TXT records showing SPF and DMARC"),
    "4.7":  (os.path.join(SHOTS,"fig47_wildcard_dns.png"),     "Figure 4.7: Wildcard DNS — randomxyz123.neuralsh.com resolves to origin IP"),
    "4.8":  (os.path.join(SHOTS,"fig48_ssl_cert.png"),         "Figure 4.8: SSL certificate mismatch — endoncambodia.com and onesala.com"),
    "4.9":  (os.path.join(SHOTS,"fig49_nmap.png"),             "Figure 4.9: Nmap full port scan of 103.16.62.217 — twenty-three open ports"),
    "4.10": (os.path.join(SHOTS,"fig410_cpanel_whm.png"),      "Figure 4.10: cPanel and WHM login pages accessible from the public internet"),
    "4.11": (os.path.join(SHOTS,"fig411_mikrotik.png"),        "Figure 4.11: MikroTik RouterOS curl response confirming WebFig accessibility"),
    "4.12": (os.path.join(SHOTS,"fig412_nikto.png"),           "Figure 4.12: Nikto web scanner results"),
    "4.13": (os.path.join(SHOTS,"fig413_nuclei.png"),          "Figure 4.13: Nuclei scan — zero matches (Cloudflare WAF absorbing probes)"),
    "4.14": (os.path.join(SHOTS,"fig414_burp_waf.png"),        "Figure 4.14: Burp Suite — cloudflare vs direct origin confirming WAF bypass"),
    "4.15": (os.path.join(SHOTS,"fig415_ratelimit.png"),       "Figure 4.15: Rate limit bypass — fifty/fifty tokens, zero rate-limit responses"),
    "4.16": (os.path.join(SHOTS,"fig416_jwt_404.png"),         "Figure 4.16: JWT endpoint confirmed live (HTTP 200) as of eleven June 2026"),
    "4.17": (os.path.join(SHOTS,"fig417_whm_browser.png"),     "Figure 4.17: WHM admin panel at 103.16.62.217:2087 — publicly accessible"),
    "4.18": (os.path.join(SHOTS,"fig418_mikrotik_browser.png"),"Figure 4.18: MikroTik WebFig — RouterOS v6.49.18, admin pre-filled"),
    "4.19": (os.path.join(SHOTS,"fig419_mysql_connect.png"),   "Figure 4.19: MySQL connection from public IP — authentication prompt exposed"),
    "4.22": (os.path.join(SHOTS,"fig422_attack_chains.png"),   "Figure 4.22: Attack chain diagram — four confirmed attack vectors"),
}

LOGO_MAP = {
    "nmap":        os.path.join(IMGS, "nmap_logo.png"),
    "burpsuite":   os.path.join(IMGS, "burpsuite_logo.png"),
    "metasploit":  os.path.join(IMGS, "metasploit_logo.png"),
    "nikto":       os.path.join(IMGS, "nikto_logo.png"),
    "nuclei":      os.path.join(IMGS, "nuclei_logo.png"),
    "cloudflare":  os.path.join(IMGS, "cloudflare_logo.png"),
}

# ── Front matter ──────────────────────────────────────────────────────────────
def add_front_matter(doc):
    # ── Title page ─────────────────────────────────────────────────────────
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_after = Pt(24)
    logo = os.path.join(IMGS, "itc_logo.png")
    if os.path.exists(logo):
        p.add_run().add_picture(logo, width=Cm(3))

    def centre(text, size=12, bold=False, space_after=6):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_after = Pt(space_after)
        r = p.add_run(text)
        fmt(r, size=size, bold=bold)

    centre("INSTITUTION OF TECHNOLOGY OF CAMBODIA", 14, bold=True, space_after=4)
    centre("Department of General Studies and Natural Sciences", 12, space_after=4)
    centre("Bachelor of Information and Communication Engineering", 12, space_after=24)
    centre("INTERNSHIP REPORT", 16, bold=True, space_after=12)
    centre("VULNERABILITY ASSESSMENT AND PENETRATION TESTING (VAPT)", 14, bold=True, space_after=6)
    centre("ON A WEB APPLICATION", 14, bold=True, space_after=6)
    centre("A Case Study of neuralsh.com", 12, space_after=24)

    # Internship details table
    tbl = doc.add_table(rows=5, cols=2)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    rows_data = [
        ("Student Name:",       "[Your Full Name]"),
        ("Student ID:",         "[Your Student ID]"),
        ("Academic Supervisor:","[Supervisor Name]"),
        ("Company Supervisor:", "Prestige Alliance Co., Ltd."),
        ("Submission Date:",    "June 2026"),
    ]
    for ri, (lbl, val) in enumerate(rows_data):
        lc = tbl.cell(ri, 0)
        vc = tbl.cell(ri, 1)
        lc.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        vc.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        fmt(lc.paragraphs[0].add_run(lbl), size=12, bold=True)
        fmt(vc.paragraphs[0].add_run(val), size=12)
    doc.add_paragraph()

    # ── Acknowledgment ─────────────────────────────────────────────────────
    ch_head(doc, "ACKNOWLEDGMENT")
    body(doc, "I would like to express my sincere gratitude to the President of the Institution of Technology of Cambodia, the Head of the Department of General Studies and Natural Sciences, and my academic supervisor for their continuous guidance and support throughout this internship programme.")
    body(doc, "I am deeply grateful to the management and technical team at Prestige Alliance Co., Ltd. for providing the opportunity to conduct this vulnerability assessment and penetration testing engagement on neuralsh.com, and for their professional guidance during the internship period.")
    body(doc, "I also extend my appreciation to all colleagues and peers who provided feedback during the preparation of this report.")

    # ── Khmer Abstract (មូលដ្ឋានទេច) ─────────────────────────────────────────
    # ITC requires a Khmer-language summary as page II of front matter.
    # The heading uses Khmer OS font; paste your Khmer text in place of the placeholder.
    p_kh = doc.add_paragraph(style='Heading 1')
    p_kh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rk = p_kh.add_run("មូលដ្ឋានទេច")
    rk.font.name = "Khmer OS"          # requires Khmer OS or Khmer UI font
    rk.font.size = Pt(16)
    rk.font.bold = True
    rk.font.color.rgb = RGBColor(0, 0, 0)

    p_kh_body = doc.add_paragraph()
    p_kh_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kh_body.paragraph_format.first_line_indent = Cm(1.27)
    p_kh_body.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p_kh_body.paragraph_format.space_after = Pt(6)
    r_kh = p_kh_body.add_run(
        "[បញ្ចូលសរុបខ្លឹមសារជាភាសាខ្មែររបស់អ្នកនៅទីនេះ។ "
        "ចម្លងអត្ថបទខ្មែររបស់អ្នកហើយជំនួសអត្ថបទក្នុងតង្កៀបនេះ។]"
    )
    r_kh.font.name = "Khmer OS"
    r_kh.font.size = Pt(12)

    # ── Abstract ────────────────────────────────────────────────────────────
    ch_head(doc, "ABSTRACT")
    body(doc, "This report presents a comprehensive Vulnerability Assessment and Penetration Testing (VAPT) engagement conducted on neuralsh.com, an AI-powered neural search platform, as part of an internship at Prestige Alliance Co., Ltd. The assessment was authorized in writing prior to testing, and all activities were conducted in accordance with the OWASP Testing Guide and established ethical hacking standards.")
    body(doc, "A black-box methodology was applied, simulating an external attacker with no prior knowledge of the target system. The engagement followed the complete penetration testing lifecycle: reconnaissance, scanning, enumeration, exploitation, post-exploitation, and reporting. Twenty (twenty) distinct vulnerabilities were discovered: four Critical, five High, seven Medium, and four Low severity findings. Critical findings include a publicly exposed MySQL database, a MikroTik network router administration panel, a cPanel hosting control panel, and a WHM root server administration panel — all accessible from the public internet without IP restriction.")
    body(doc, "A rate-limiting control was successfully bypassed via HTTP header spoofing, enabling unlimited API token generation. A follow-up verification scan conducted on ten June 2026 confirmed all original findings remained unpatched and identified three additional findings.")
    body(doc, "Keywords: Penetration Testing, VAPT, Web Application Security, OWASP, Rate Limiting Bypass, JWT Analysis, cPanel Exposure, MikroTik, Black Box Testing, CVSS v3.1")

    # ── Table of Contents ───────────────────────────────────────────────────
    ch_head(doc, "TABLE OF CONTENTS")
    add_toc_field(doc)

    # ── List of Figures ─────────────────────────────────────────────────────
    ch_head(doc, "LIST OF FIGURES")
    figures = [
        ("Figure 4.2",  "SSH connection to Kali Linux VM"),
        ("Figure 4.3",  "Tool version verification — Nmap, Nikto, Metasploit"),
        ("Figure 4.4",  "neuralsh.com homepage"),
        ("Figure 4.5",  "WHOIS lookup for neuralsh.com"),
        ("Figure 4.6",  "DNS enumeration — MX and TXT records (SPF, DMARC)"),
        ("Figure 4.7",  "Wildcard DNS — randomxyz123.neuralsh.com resolving to origin IP"),
        ("Figure 4.8",  "SSL certificate mismatch on origin server"),
        ("Figure 4.9",  "Nmap full port scan of 103.16.62.217 — twenty-three open ports"),
        ("Figure 4.10", "cPanel and WHM login pages publicly accessible"),
        ("Figure 4.11", "MikroTik RouterOS WebFig accessibility confirmation"),
        ("Figure 4.12", "Nikto web scanner results"),
        ("Figure 4.13", "Nuclei scan — zero matches"),
        ("Figure 4.14", "Burp Suite — Cloudflare WAF bypass confirmation"),
        ("Figure 4.15", "Rate limit bypass — fifty/fifty tokens, zero rate-limit responses"),
        ("Figure 4.16", "JWT endpoint confirmed live as of eleven June 2026"),
        ("Figure 4.17", "WHM admin panel publicly accessible at port 2087"),
        ("Figure 4.18", "MikroTik WebFig login with admin pre-filled"),
        ("Figure 4.19", "MySQL connection from public IP"),
        ("Figure 4.22", "Attack chain diagram — four confirmed attack vectors"),
    ]
    tbl = doc.add_table(rows=len(figures), cols=2)
    tbl.style = 'Table Grid'
    for ri, (fig, desc) in enumerate(figures):
        tbl.cell(ri, 0).paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        tbl.cell(ri, 1).paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        fmt(tbl.cell(ri, 0).paragraphs[0].add_run(fig),  size=11, bold=True)
        fmt(tbl.cell(ri, 1).paragraphs[0].add_run(desc), size=11)
    doc.add_paragraph()

    # ── List of Tables ──────────────────────────────────────────────────────
    ch_head(doc, "LIST OF TABLES")
    tables_list = [
        ("Table 4.1",  "Testing tools used in this engagement"),
        ("Table 5.1",  "Complete findings register — twenty vulnerabilities"),
        ("Table 5.2",  "Severity distribution and CVSS score summary"),
        ("Table 5.3",  "Remediation priority roadmap"),
    ]
    tbl2 = doc.add_table(rows=len(tables_list), cols=2)
    tbl2.style = 'Table Grid'
    for ri, (tname, desc) in enumerate(tables_list):
        tbl2.cell(ri, 0).paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        tbl2.cell(ri, 1).paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        fmt(tbl2.cell(ri, 0).paragraphs[0].add_run(tname), size=11, bold=True)
        fmt(tbl2.cell(ri, 1).paragraphs[0].add_run(desc),  size=11)
    doc.add_paragraph()

    # ── List of Abbreviations ───────────────────────────────────────────────
    ch_head(doc, "LIST OF ABBREVIATIONS")
    abbrevs = [
        ("API",   "Application Programming Interface"),
        ("CDN",   "Content Delivery Network"),
        ("CORS",  "Cross-Origin Resource Sharing"),
        ("CSP",   "Content Security Policy"),
        ("CVSS",  "Common Vulnerability Scoring System"),
        ("CWE",   "Common Weakness Enumeration"),
        ("DMARC", "Domain-based Message Authentication, Reporting and Conformance"),
        ("DNS",   "Domain Name System"),
        ("HTTP",  "Hypertext Transfer Protocol"),
        ("HTTPS", "Hypertext Transfer Protocol Secure"),
        ("ITC",   "Institution of Technology of Cambodia"),
        ("JWT",   "JSON Web Token"),
        ("NIST",  "National Institute of Standards and Technology"),
        ("OSINT", "Open Source Intelligence"),
        ("OWASP", "Open Web Application Security Project"),
        ("SMTP",  "Simple Mail Transfer Protocol"),
        ("SPF",   "Sender Policy Framework"),
        ("SQL",   "Structured Query Language"),
        ("SSL",   "Secure Sockets Layer"),
        ("TCP",   "Transmission Control Protocol"),
        ("TLS",   "Transport Layer Security"),
        ("URL",   "Uniform Resource Locator"),
        ("VAPT",  "Vulnerability Assessment and Penetration Testing"),
        ("WAF",   "Web Application Firewall"),
        ("WHM",   "Web Host Manager"),
        ("XFF",   "X-Forwarded-For (HTTP header)"),
        ("XSS",   "Cross-Site Scripting"),
    ]
    tbl3 = doc.add_table(rows=len(abbrevs), cols=2)
    tbl3.style = 'Table Grid'
    for ri, (abbr, full) in enumerate(abbrevs):
        tbl3.cell(ri, 0).paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        tbl3.cell(ri, 1).paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        fmt(tbl3.cell(ri, 0).paragraphs[0].add_run(abbr), size=11, bold=True)
        fmt(tbl3.cell(ri, 1).paragraphs[0].add_run(full), size=11)
    doc.add_paragraph()

    # Page-number section break: switch to Arabic at start of Chapter I
    add_section_break(doc, restart_arabic=True)

# ── Markdown → docx ───────────────────────────────────────────────────────────
def process_md(doc):
    with open(MD, encoding='utf-8') as fh:
        lines = fh.readlines()

    in_code  = False
    code_buf = []
    in_table = False
    table_rows = []
    in_53    = False   # True after ## 5.3 — use cards instead of prose

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
            i += 1; continue
        if in_code:
            code_buf.append(line)
            i += 1; continue

        # ── separator ──────────────────────────────────────────────────────
        if stripped in ('---', '***', '___'):
            i += 1; continue

        # ── markdown tables ────────────────────────────────────────────────
        if stripped.startswith('|') and stripped.endswith('|'):
            cols = [c.strip() for c in stripped[1:-1].split('|')]
            if not all(re.fullmatch(r':?-+:?', c.replace(' ','')) for c in cols):
                table_rows.append(cols)
            in_table = True
            i += 1; continue
        else:
            if in_table:
                if not in_53:
                    md_table(doc, table_rows)
                table_rows = []
                in_table = False

        # ── figure placeholders ─────────────────────────────────────────────
        m = re.match(r'\*\[Figure (4\.\d+(?:\.\d+)?):.*?\]\*', stripped)
        if m:
            key = m.group(1)
            if key in IMG_MAP:
                path, cap = IMG_MAP[key]
                add_img(doc, path, cap)
            i += 1; continue

        # ── headings ───────────────────────────────────────────────────────
        if stripped.startswith('#### '):
            sec_head(doc, stripped[5:], level=3)
            i += 1; continue

        if stripped.startswith('### '):
            txt = stripped[4:]
            # detect 5.3 — switch to card mode
            if re.match(r'^5\.3\b', txt):
                in_53 = True
                sec_head(doc, txt, level=1)
                # Insert all finding cards
                for f in FINDINGS:
                    finding_card(doc, f)
                # skip the original prose for 5.3
                i += 1
                while i < len(lines):
                    l2 = lines[i].strip()
                    if re.match(r'^#{2,3}\s+5\.[4-9]', l2) or re.match(r'^#{1,3}\s+6\.', l2):
                        in_53 = False
                        break
                    i += 1
                continue
            sec_head(doc, txt, level=2)
            i += 1; continue

        if stripped.startswith('## '):
            txt = stripped[3:]
            in_53 = False
            # Map chapter breaks
            ch_breaks = ['4.1 ', '5.1 ', '6.1 ', '6. ']
            if any(txt.startswith(k) for k in ch_breaks):
                pass
            sec_head(doc, txt, level=1)
            i += 1; continue

        if stripped.startswith('# '):
            ch_head(doc, stripped[2:])
            i += 1; continue

        # ── bullet list ────────────────────────────────────────────────────
        m_b = re.match(r'^[-*]\s+(.+)', stripped)
        if m_b and not in_53:
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.left_indent = Cm(1.27)
            p.paragraph_format.first_line_indent = Cm(0)
            r = p.add_run(m_b.group(1).strip())
            fmt(r, size=12)
            i += 1; continue

        # ── skip front-matter meta lines ────────────────────────────────────
        if stripped.startswith('**Student') or stripped.startswith('**Submission') \
           or stripped.startswith('**Program') or stripped.startswith('**Institution') \
           or stripped.startswith('**Supervisor') or stripped.startswith('> '):
            i += 1; continue

        # ── blank / separator lines ─────────────────────────────────────────
        if not stripped:
            i += 1; continue

        # ── skip sections already in front matter ───────────────────────────
        if stripped.startswith('## Declaration') or stripped.startswith('## Abstract') \
           or stripped.startswith('## Table of Contents'):
            # skip until next ## heading
            i += 1
            while i < len(lines):
                if lines[i].startswith('## ') or lines[i].startswith('# '):
                    break
                i += 1
            continue

        # ── skip finding prose in 5.3 (replaced by cards) ──────────────────
        if in_53:
            i += 1; continue

        # ── normal paragraph (strip inline markdown) ────────────────────────
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', stripped)
        clean = re.sub(r'\*([^*]+)\*',     r'\1', clean)
        clean = re.sub(r'`([^`]+)`',       r'\1', clean)
        clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)
        if clean.strip():
            body(doc, clean)
        i += 1

# ── Build document ────────────────────────────────────────────────────────────
def build():
    doc = new_doc()
    add_front_matter(doc)
    process_md(doc)
    doc.save(OUT)
    print(f"Saved → {OUT}")
    print("NOTE: Open the .docx in Word, press Ctrl+A then F9 to update the Table of Contents.")

if __name__ == '__main__':
    build()
