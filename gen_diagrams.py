#!/usr/bin/env python3
"""Generate crisp full-width diagram PNGs for the VAPT thesis."""

from PIL import Image, ImageDraw, ImageFont
import os

OUT   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image")
FONT  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def f(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)

# ── colours ──────────────────────────────────────────────────────────────────
WHITE  = (255,255,255)
DARK   = (30, 30, 60)
BLUE   = (46,116,181)
BLUE2  = (68,114,196)
PURPLE = (112,48,160)
RED    = (192,0,0)
ORANGE = (220,120,0)
GREEN  = (84,130,53)
BROWN  = (155,99,61)
GREY   = (180,180,180)
LGREY  = (240,240,240)
DGREY  = (80,80,80)

W = 1260   # px — matches 16 cm @ 200 dpi

def save(img, name):
    p = os.path.join(OUT, name)
    img.save(p, dpi=(200,200))
    print(f"  ✓  {p}")

def text_center(d, cx, cy, txt, fnt, fill):
    """Draw single-line text centred on (cx, cy)."""
    bb = d.textbbox((0,0), txt, font=fnt)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    d.text((cx - tw//2, cy - th//2), txt, font=fnt, fill=fill)

def text_block(d, cx, top, lines, fnt, fill, leading=4):
    """Draw multi-line text centred horizontally, starting at top y."""
    for i, ln in enumerate(lines):
        bb = d.textbbox((0,0), ln, font=fnt)
        tw = bb[2]-bb[0]; th = bb[3]-bb[1]
        d.text((cx - tw//2, top + i*(th+leading)), ln, font=fnt, fill=fill)

def rbox(d, x, y, w, h, fill, outline=None, r=8):
    d.rounded_rectangle([x,y,x+w,y+h], radius=r, fill=fill,
                        outline=outline or fill, width=2)

def arrow_h(d, x1, x2, y, col=DGREY):
    d.line([x1, y, x2-8, y], fill=col, width=2)
    d.polygon([x2-8,y-5, x2-8,y+5, x2,y], fill=col)

def arrow_v(d, x, y1, y2, col=DGREY):
    d.line([x, y1, x, y2-8], fill=col, width=2)
    d.polygon([x-5,y2-8, x+5,y2-8, x,y2], fill=col)


# ══════════════════════════════════════════════════════════════════════════════
# Figure 7 — Penetration Testing Process Flowchart
# ══════════════════════════════════════════════════════════════════════════════
def draw_pentest_flow():
    phases = [
        ("1","RECONNAISSANCE",         ["WHOIS · DNS · SSL certs","JS bundle analysis · Shodan"],  BLUE),
        ("2","SCANNING &\nENUMERATION",["Nmap port scan · Nikto","Directory brute-force"],          BLUE2),
        ("3","VULNERABILITY\nASSESSMENT",["OWASP mapping · CVSS","Manual + automated tests"],      PURPLE),
        ("4","EXPLOITATION",           ["Rate-limit bypass","JWT farming · Admin panels"],          RED),
        ("5","POST-EXPLOITATION",      ["Lateral movement analysis","Follow-up scan"],             BROWN),
    ]

    TITLE_H = 46
    BH      = 120      # box height
    ARROW   = 24
    M       = 28       # side margin
    REP_H   = 72
    GAP_V   = 36       # vertical gap between phases row and report
    TOTAL_H = TITLE_H + BH + GAP_V + REP_H + M

    avail = W - 2*M - 4*ARROW
    BW = avail // 5

    img = Image.new("RGB", (W, TOTAL_H), WHITE)
    d   = ImageDraw.Draw(img)

    # title bar
    rbox(d, 0, 0, W, TITLE_H, DARK, r=0)
    text_center(d, W//2, TITLE_H//2, "Penetration Testing Process — Black-Box Methodology", f(20,True), WHITE)

    # phase boxes
    x = M
    cy_row = TITLE_H + BH//2

    for idx,(num, name, details, col) in enumerate(phases):
        rbox(d, x, TITLE_H, BW, BH, col, r=6)
        # circle number
        nd = 26
        nx, ny = x+nd//2+6, TITLE_H+nd//2+6
        d.ellipse([nx-nd//2,ny-nd//2,nx+nd//2,ny+nd//2], fill=WHITE)
        text_center(d, nx, ny, num, f(14,True), col)
        # name (may be 2 lines)
        name_lines = name.split("\n")
        text_block(d, x+BW//2, TITLE_H+10, name_lines, f(13,True), WHITE, leading=3)
        # detail lines
        det_y = TITLE_H + 10 + len(name_lines)*17 + 6
        text_block(d, x+BW//2, det_y, details, f(11), (230,230,230), leading=4)
        # arrow
        if idx < 4:
            arrow_h(d, x+BW, x+BW+ARROW, cy_row)
        x += BW + ARROW

    # report box
    rw = BW + 80
    rx = (W - rw) // 2
    ry = TITLE_H + BH + GAP_V
    rbox(d, rx, ry, rw, REP_H, DARK, r=8)
    text_center(d, rx+rw//2, ry+18, "VAPT REPORT", f(16,True), WHITE)
    text_block(d, rx+rw//2, ry+38,
               ["Full findings register · CVSS v3.1 scores · Remediation roadmap"], f(11), GREY)

    # downward arrow to report
    arrow_v(d, W//2, TITLE_H+BH+4, ry)

    save(img, "pentest_flow_new.png")


# ══════════════════════════════════════════════════════════════════════════════
# Figure 5.1 — Recommended Network Security Architecture
# ══════════════════════════════════════════════════════════════════════════════
def draw_architecture():
    TITLE_H = 46
    BH      = 72
    BW      = 180
    ARROW   = 26
    M       = 20
    SEC_GAP = 20       # gap between sections
    SEC_LH  = 22       # section label height

    # Row 1 — traffic flow (5 boxes + 4 arrows)
    n1 = 5
    avail1 = W - 2*M - (n1-1)*ARROW
    bw1 = avail1 // n1

    row1 = [
        ("Internet","External\nusers",             (200,200,200), DARK),
        ("Cloudflare WAF","DDoS · Bot filter\nRate limiting",  BLUE,  WHITE),
        ("Origin Server","HTTPS only\nIP restricted",          BLUE2, WHITE),
        ("Web Application","Nuxt.js\nneuralsh.com",            PURPLE,WHITE),
        ("MySQL Database","Private network\nonly · no public port",GREEN,WHITE),
    ]

    # Row 2 — admin panels (5 boxes)
    n2 = 5
    avail2 = W - 2*M - (n2-1)*12
    bw2 = avail2 // n2

    row2 = [
        ("WHM / cPanel",    "Port 2087/2083\nIP allowlist only",       RED),
        ("MikroTik Admin",  "Port 8291\nVPN access only",              ORANGE),
        ("MySQL Service",   "Port 3306\nPrivate net only",             BLUE),
        ("SSH Jump Host",   "MFA + audit log\nNo direct SSH",          GREEN),
        ("PowerDNS Admin",  "Port 53/API\nInternal VLAN only",         PURPLE),
    ]

    # Row 3 — security controls (4 boxes)
    n3 = 4
    avail3 = W - 2*M - (n3-1)*12
    bw3 = avail3 // n3
    row3 = [
        (BLUE2,  "HSTS + CSP Headers",    ["Strict-Transport-Security","Content-Security-Policy"]),
        (PURPLE, "DMARC p=reject",         ["SPF + DKIM + DMARC","Email spoofing prevention"]),
        (DARK,   "JWT Secret Rotation",    ["HS256 → RS256","Short expiry + revocation"]),
        (GREEN,  "Disable Dir. Listing",   ["Apache: Options -Indexes","Remove server version"]),
    ]

    bh3 = 80
    row1_y = TITLE_H + SEC_LH + 6
    row2_y = row1_y + BH + SEC_GAP + SEC_LH + 6
    row3_y = row2_y + BH + SEC_GAP + SEC_LH + 6
    FOOT_H = 28
    TOTAL_H = row3_y + bh3 + M + FOOT_H

    img = Image.new("RGB", (W, TOTAL_H), WHITE)
    d   = ImageDraw.Draw(img)

    # title
    rbox(d, 0, 0, W, TITLE_H, DARK, r=0)
    text_center(d, W//2, TITLE_H//2,
                "Recommended Network Security Architecture — neuralsh.com", f(18,True), WHITE)

    # ── Row 1 label + boxes ──────────────────────────────────────────────────
    text_center(d, W//2, TITLE_H+SEC_LH//2+2, "▶  Traffic Flow (Internet → Application → Database)", f(12,True), DARK)
    x = M
    for i,(title, sub, col, tcol) in enumerate(row1):
        rbox(d, x, row1_y, bw1, BH, col, r=6)
        text_block(d, x+bw1//2, row1_y+10, [title], f(13,True), tcol)
        text_block(d, x+bw1//2, row1_y+32, sub.split("\n"), f(10), (230,230,230) if tcol==WHITE else (80,80,80))
        if i < n1-1:
            arrow_h(d, x+bw1, x+bw1+ARROW, row1_y+BH//2)
        x += bw1 + ARROW

    # ── Row 2 label + boxes ──────────────────────────────────────────────────
    text_center(d, W//2, row1_y+BH+SEC_GAP//2+4, "🔒  Restricted Administrative Access (All panels off public internet)", f(12,True), RED)
    x = M
    for title, sub, col in row2:
        rbox(d, x, row2_y, bw2, BH, col, r=6)
        text_block(d, x+bw2//2, row2_y+10, [title], f(12,True), WHITE)
        text_block(d, x+bw2//2, row2_y+32, sub.split("\n"), f(10), (230,230,230))
        x += bw2 + 12

    # ── Row 3 label + boxes ──────────────────────────────────────────────────
    text_center(d, W//2, row2_y+BH+SEC_GAP//2+4, "🛡  Application Security Controls", f(12,True), PURPLE)
    x = M
    for col, title, lines in row3:
        rbox(d, x, row3_y, bw3, bh3, col, r=6)
        text_block(d, x+bw3//2, row3_y+10, [title], f(12,True), WHITE)
        text_block(d, x+bw3//2, row3_y+32, lines, f(10), (230,230,230))
        x += bw3 + 12

    # footer
    fy = row3_y + bh3 + M
    rbox(d, 0, fy, W, FOOT_H, DARK, r=0)
    text_center(d, W//2, fy+FOOT_H//2,
                "Prestige Alliance Co., Ltd. — VAPT Remediation Architecture — neuralsh.com", f(11), GREY)

    save(img, "recommended_architecture_new.png")


# ══════════════════════════════════════════════════════════════════════════════
# Figure 2 — Org Chart
# ══════════════════════════════════════════════════════════════════════════════
def draw_org_chart():
    TITLE_H = 46
    BW, BH  = 180, 60
    M       = 20
    FOOT_H  = 26

    rows = [
        # (cx_fraction_of_W, label_line1, label_line2, colour)
        [(0.5, "Chief Executive Officer", "Prestige Alliance Co., Ltd.", DARK)],
        [(0.25, "Technical Director", "IT & Cybersecurity", BLUE),
         (0.5,  "Operations Director", "HR & Finance",       BLUE),
         (0.75, "Business Development", "Sales & Partners",   BLUE)],
        [(0.125, "Red Team", "Penetration Testing & VAPT", PURPLE),
         (0.30,  "Blue Team", "SOC · Monitoring",           BLUE2),
         (0.475, "Dev Team", "Software & Integration",      (68,130,100))],
        [(0.125, "Security Intern", "VAPT · neuralsh.com",  BROWN)],
    ]

    row_ys = [TITLE_H+46, TITLE_H+160, TITLE_H+274, TITLE_H+388]
    TOTAL_H = row_ys[-1] + BH + M + FOOT_H

    img = Image.new("RGB", (W, TOTAL_H), WHITE)
    d   = ImageDraw.Draw(img)

    # title
    rbox(d, 0, 0, W, TITLE_H, DARK, r=0)
    text_center(d, W//2, TITLE_H//2,
                "Prestige Alliance Co., Ltd. — Organisational Structure", f(18,True), WHITE)

    prev_cxs = []
    for ri, (row, ry) in enumerate(zip(rows, row_ys)):
        cxs = [int(fr*W) for fr,*_ in row]

        # vertical connector from parent
        if ri > 0 and prev_cxs:
            # horizontal bar at midpoint between rows
            mid_y = (row_ys[ri-1] + BH + ry) // 2
            # which parent drives this row
            if ri == 1:
                par = [int(0.5*W)]
            elif ri == 2:
                par = [int(0.25*W)]
            elif ri == 3:
                par = [int(0.125*W)]
            else:
                par = prev_cxs

            # vertical from parent down to midline
            for px in par:
                d.line([px, row_ys[ri-1]+BH, px, mid_y], fill=GREY, width=2)
            # horizontal bar
            if len(cxs) > 1:
                d.line([cxs[0], mid_y, cxs[-1], mid_y], fill=GREY, width=2)
            # verticals down to each child
            for cx in cxs:
                d.line([cx, mid_y, cx, ry], fill=GREY, width=2)
            # dots at junction
            for cx in cxs:
                r2=5; d.ellipse([cx-r2,mid_y-r2,cx+r2,mid_y+r2], fill=BLUE)

        # draw boxes
        for fr, l1, l2, col in row:
            cx = int(fr*W)
            rbox(d, cx-BW//2, ry, BW, BH, col, r=8)
            text_block(d, cx, ry+10, [l1], f(13,True), WHITE)
            text_block(d, cx, ry+32, [l2], f(10), (220,220,220))

        prev_cxs = cxs

    # footer
    fy = row_ys[-1] + BH + M
    rbox(d, 0, fy, W, FOOT_H, DARK, r=0)
    text_center(d, W//2, fy+FOOT_H//2,
                "Prestige Alliance Co., Ltd. · info@prestigealliance.co · +855-88-288-2289", f(11), GREY)

    save(img, "org_chart_new.png")


if __name__ == "__main__":
    print("Generating diagrams...")
    draw_pentest_flow()
    draw_architecture()
    draw_org_chart()
    print("Done.")
