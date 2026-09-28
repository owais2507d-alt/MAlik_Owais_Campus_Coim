# -*- coding: utf-8 -*-
"""Campus Coin — full project PowerPoint deck."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

SHOTS = r"D:\campus-coin-master\ppt\screenshots"
OUT = r"D:\campus-coin-master\Campus-Coin-Team-Bombers.pptx"

# palette
BG      = RGBColor(0x0C, 0x0C, 0x10)
PANEL   = RGBColor(0x17, 0x17, 0x1E)
PANEL2  = RGBColor(0x1F, 0x1F, 0x28)
HONEY   = RGBColor(0xF5, 0x9E, 0x0B)
HONEY_L = RGBColor(0xFB, 0xBF, 0x24)
TEXT    = RGBColor(0xFA, 0xFA, 0xFA)
MUTED   = RGBColor(0xA1, 0xA1, 0xAA)
GREEN   = RGBColor(0x10, 0xB9, 0x81)
ROSE    = RGBColor(0xF4, 0x3F, 0x5E)
BLUE    = RGBColor(0x3B, 0x82, 0xF6)
LINE    = RGBColor(0x3F, 0x3F, 0x4E)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = 13.333, 7.5


def slide():
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = BG
    bg.line.fill.background()
    bg.shadow.inherit = False
    return s


def box(s, x, y, w, h, fill=PANEL, line=None, radius=True):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                             Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line:
        shp.line.color.rgb = line; shp.line.width = Pt(1.25)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    if radius:
        try:
            shp.adjustments[0] = 0.06
        except Exception:
            pass
    return shp


def txt(s, x, y, w, h, text, size=14, color=TEXT, bold=False, align=PP_ALIGN.LEFT,
        font="Segoe UI", anchor=MSO_ANCHOR.TOP, line_spacing=1.05):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = color; r.font.name = font
    return tb


def rich(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """runs = list of paragraphs; each paragraph = list of (text,size,color,bold)"""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = 1.08
        for (t, sz, c, b) in para:
            r = p.add_run(); r.text = t
            r.font.size = Pt(sz); r.font.color.rgb = c; r.font.bold = b
            r.font.name = "Segoe UI"
    return tb


def header(s, title, kicker="CAMPUS COIN"):
    # accent bar
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(0.42), Inches(0.14), Inches(0.62))
    bar.fill.solid(); bar.fill.fore_color.rgb = HONEY; bar.line.fill.background(); bar.shadow.inherit = False
    txt(s, 0.85, 0.30, 9.5, 0.3, kicker, 10, HONEY, True)
    txt(s, 0.85, 0.52, 11.6, 0.55, title, 26, TEXT, True)
    # thin line
    ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(1.12), Inches(12.23), Pt(1.2))
    ln.fill.solid(); ln.fill.fore_color.rgb = LINE; ln.line.fill.background(); ln.shadow.inherit = False


def footer(s, n, total=25):
    txt(s, 0.55, 7.12, 6, 0.3, "Campus Coin · NextGen BudgetBee — Full Project Walkthrough", 9, MUTED)
    txt(s, 11.5, 7.12, 1.3, 0.3, f"{n} / {total}", 9, MUTED, align=PP_ALIGN.RIGHT)


def pic(s, name, x, y, w, border=True):
    path = os.path.join(SHOTS, name)
    p = s.shapes.add_picture(path, Inches(x), Inches(y), width=Inches(w))
    if border:
        fr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                Inches(x) - Pt(2), Inches(y) - Pt(2),
                                p.width + Pt(4), p.height + Pt(4))
        fr.fill.background()
        fr.line.color.rgb = LINE; fr.line.width = Pt(1.5)
        fr.shadow.inherit = False
        # send frame behind picture
        sp = fr._element; sp.getparent().remove(sp)
        p._element.addprevious(sp)
    return p


def chip(s, x, y, w, h, label, color=HONEY, tcolor=RGBColor(0x1A, 0x12, 0x00), size=10.5, bold=True):
    c = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    c.fill.solid(); c.fill.fore_color.rgb = color; c.line.fill.background(); c.shadow.inherit = False
    try: c.adjustments[0] = 0.5
    except Exception: pass
    tf = c.text_frame; tf.word_wrap = True
    tf.margin_left = Pt(2); tf.margin_right = Pt(2); tf.margin_top = Pt(1); tf.margin_bottom = Pt(1)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = tcolor; r.font.name = "Segoe UI"
    return c


def bullets(s, x, y, w, h, items, size=12.5, gap_color=HONEY):
    """items: list of (head, body) or plain str"""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.12; p.space_after = Pt(5)
        r0 = p.add_run(); r0.text = "▸ "
        r0.font.size = Pt(size); r0.font.color.rgb = gap_color; r0.font.bold = True; r0.font.name = "Segoe UI"
        if isinstance(it, tuple):
            head, body = it
            r1 = p.add_run(); r1.text = head
            r1.font.size = Pt(size); r1.font.bold = True; r1.font.color.rgb = TEXT; r1.font.name = "Segoe UI"
            r2 = p.add_run(); r2.text = "  " + body
            r2.font.size = Pt(size); r2.font.color.rgb = MUTED; r2.font.name = "Segoe UI"
        else:
            r1 = p.add_run(); r1.text = it
            r1.font.size = Pt(size); r1.font.color.rgb = TEXT; r1.font.name = "Segoe UI"
    return tb


def table(s, x, y, w, rows, col_w=None, header_color=HONEY, fsize=10.5, hsize=11, row_h=0.32, hrow_h=0.36):
    n_rows, n_cols = len(rows), len(rows[0])
    g = s.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(hrow_h + row_h * (n_rows - 1)))
    tbl = g.table
    # style: kill banding
    tbl.first_row = True
    if col_w:
        total = sum(col_w)
        for i, cw in enumerate(col_w):
            tbl.columns[i].width = Emu(int(Inches(w) * cw / total))
    tbl.rows[0].height = Inches(hrow_h)
    for i in range(1, n_rows):
        tbl.rows[i].height = Inches(row_h)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.text = ""
            cell.margin_left = Pt(6); cell.margin_right = Pt(4)
            cell.margin_top = Pt(2); cell.margin_bottom = Pt(2)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            r = p.add_run(); r.text = str(val)
            r.font.name = "Segoe UI"
            if ri == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = header_color
                r.font.size = Pt(hsize); r.font.bold = True
                r.font.color.rgb = RGBColor(0x1A, 0x12, 0x00)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = PANEL if ri % 2 else PANEL2
                r.font.size = Pt(fsize)
                r.font.color.rgb = TEXT if ci == 0 else MUTED
                if ci == 0: r.font.bold = True
    return g


def arrow(s, x, y, w, h, color=HONEY):
    a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    a.fill.solid(); a.fill.fore_color.rgb = color; a.line.fill.background(); a.shadow.inherit = False
    return a


TOTAL = 26
n = 0

# ============================================================ 1 TITLE
n += 1
s = slide()
# big honey block left
blk = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.35), prs.slide_height)
blk.fill.solid(); blk.fill.fore_color.rgb = HONEY; blk.line.fill.background(); blk.shadow.inherit = False
chip(s, 1.0, 1.55, 2.6, 0.42, "FULL PROJECT WALKTHROUGH", HONEY, RGBColor(0x1A, 0x12, 0x00), 11)
txt(s, 1.0, 2.15, 11, 1.1, "Campus Coin", 54, TEXT, True)
txt(s, 1.0, 3.15, 11, 0.6, "NextGen BudgetBee — Student Budget Tracker", 22, HONEY_L, True)
chip(s, 1.0, 3.82, 2.5, 0.44, "TEAM BOMBERS", HONEY, RGBColor(0x1A, 0x12, 0x00), 13)
txt(s, 3.7, 3.86, 8.5, 0.4, "Muhammad Bilawal · Muhammad Owais · Muhammad Esam · Muhammad Muneeb · Syed Haider", 13, TEXT, True)
txt(s, 1.0, 4.5, 10.5, 0.9,
    "A complete MERN-style full-stack app: Next.js 14 client + Express MVC API + MongoDB Atlas + Socket.IO live alerts + AI (Groq / rule-based fallback).\nEvery controller, model, service, page and feature — described in one deck.",
    13.5, MUTED)
# tech chips
techs = ["Next.js 14", "React 18", "Tailwind CSS", "Express 4", "Mongoose 8", "MongoDB Atlas",
         "JWT + OTP", "Socket.IO", "Zod", "Recharts", "jsPDF", "Zustand", "Groq AI"]
cx = 1.0
for t in techs:
    w = 0.28 + 0.105 * len(t)
    if cx + w > 12.6: break
    chip(s, cx, 5.35, w, 0.36, t, PANEL2, HONEY_L, 10.5)
    cx += w + 0.14
txt(s, 1.0, 6.35, 11, 0.4, "Client :3000   ·   API :5000   ·   github.com/owais2507d-alt/MAlik_Owais_Campus_Coim", 12, MUTED)
footer(s, n, TOTAL)

# ============================================================ 2 MEET THE TEAM
n += 1
s = slide(); header(s, "Meet the Team", kicker="CAMPUS COIN · TEAM BOMBERS"); footer(s, n, TOTAL)
team = [
    ("MUHAMMAD BILAWAL", "Project Lead", "Backend & database\nAPI architecture, models,\nseeds & Atlas setup"),
    ("MUHAMMAD OWAIS", "Full-Stack Dev", "Auth, OTP, admin panel\nngrok tunnel + deployment\nGitHub / integration"),
    ("MUHAMMAD ESAM", "AI Engineer", "Categorize, insights,\nBudgetBee chat,\ntips engine"),
    ("MUHAMMAD MUNEEB", "Frontend Dev", "Dashboard, reports\ncharts, budgets UI,\ndark theme"),
    ("SYED HAIDER", "QA & Docs", "Playwright E2E suite,\nrequirement coverage,\nproject docs"),
]
cw, gap = 2.3, 0.22
x0 = (SW - (cw * 5 + gap * 4)) / 2
for i, (name, role, desc) in enumerate(team):
    x = x0 + i * (cw + gap)
    box(s, x, 1.6, cw, 4.5, PANEL, LINE)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.6), Inches(cw), Pt(4))
    bar.fill.solid(); bar.fill.fore_color.rgb = HONEY; bar.line.fill.background(); bar.shadow.inherit = False
    # avatar circle with initial
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + cw / 2 - 0.5), Inches(1.95), Inches(1.0), Inches(1.0))
    circ.fill.solid(); circ.fill.fore_color.rgb = PANEL2; circ.line.color.rgb = HONEY; circ.line.width = Pt(2)
    circ.shadow.inherit = False
    tf = circ.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = name.split()[-1][0]
    r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = HONEY_L; r.font.name = "Segoe UI"
    txt(s, x + 0.1, 3.15, cw - 0.2, 0.6, name, 12, TEXT, True, PP_ALIGN.CENTER)
    chip(s, x + 0.2, 3.75, cw - 0.4, 0.34, role, HONEY, RGBColor(0x1A, 0x12, 0x00), 10)
    txt(s, x + 0.12, 4.3, cw - 0.24, 1.7, desc, 10.5, MUTED, align=PP_ALIGN.CENTER)
box(s, x0, 6.35, cw * 5 + gap * 4, 0.55, PANEL2, LINE)
txt(s, x0 + 0.2, 6.46, cw * 5 + gap * 4 - 0.4, 0.35,
    "Campus Coin · NextGen BudgetBee — built end-to-end by Team Bombers", 12.5, HONEY_L, True, PP_ALIGN.CENTER)

# ============================================================ 2 OVERVIEW
n += 1
s = slide(); header(s, "What is Campus Coin?"); footer(s, n, TOTAL)
pic(s, "01-landing.png", 0.55, 1.35, 7.1)
box(s, 7.95, 1.35, 4.83, 5.4)
rich(s, 8.2, 1.55, 4.35, 5.0, [
    [("🎯  Purpose", 15, HONEY, True)],
    [("Budget / expense tracker built for college & university students — fast income/expense logging, student-relevant categories, per-category monthly budgets with alerts, saving tips, monthly reports with PDF export, and an AI layer.", 11.5, MUTED, False)],
    [("", 6, MUTED, False)],
    [("👥  Two roles", 15, HONEY, True)],
    [("Student — dashboard, transactions, budgets, reports, tips, AI chat", 11.5, TEXT, False)],
    [("Admin — stats, manage users / system categories / announcements", 11.5, TEXT, False)],
    [("", 6, MUTED, False)],
    [("⚡  Highlights", 15, HONEY, True)],
    [("• OTP email registration (dev shows code)", 11.5, MUTED, False)],
    [("• JWT httpOnly cookies, auto refresh on 401", 11.5, MUTED, False)],
    [("• Live budget alerts over WebSocket", 11.5, MUTED, False)],
    [("• AI categorize + monthly insights + chatbot", 11.5, MUTED, False)],
    [("• CSV import, PDF export, dark mode, streaks", 11.5, MUTED, False)],
])

# ============================================================ 3 ARCHITECTURE
n += 1
s = slide(); header(s, "System Architecture — How It All Connects"); footer(s, n, TOTAL)

def node(s, x, y, w, h, title, lines, accent=HONEY):
    box(s, x, y, w, h, PANEL, LINE)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Pt(3.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = accent; bar.line.fill.background(); bar.shadow.inherit = False
    txt(s, x + 0.12, y + 0.10, w - 0.24, 0.3, title, 12.5, accent, True)
    txt(s, x + 0.12, y + 0.42, w - 0.24, h - 0.5, lines, 10.5, MUTED)

node(s, 0.55, 1.45, 3.5, 2.5, "BROWSER (Next.js :3000)",
     "• App Router pages + route guards\n• Zustand stores (auth/ui/notifs)\n• lib/api.js fetch wrapper (cookies)\n• socket.io-client live events\n• Tailwind + Framer Motion UI", BLUE)
node(s, 0.55, 4.25, 3.5, 2.4, "AI PROVIDERS (optional)",
     "• Groq (llama-3.3-70b) primary\n• OpenRouter fallback\n• Local keyword rules always work\n• Categorize / Insights / Chat", GREEN)
node(s, 4.9, 1.45, 3.9, 5.2, "EXPRESS API (:5000)",
     "app.js → CORS → helmet → rate-limit\n        → /api/v1 router\n\nroutes/ (14 files) → validate(Zod)\n  → protect / adminOnly\n  → controllers/ (11 files)\n  → models (Mongoose) + services/\n\nsocket.io on same HTTP server\n  rooms: user:{id}\n  events: notification:new,\n  budget:updated, tx:created,\n  announcement:new", HONEY)
node(s, 9.6, 1.45, 3.18, 2.5, "MONGODB ATLAS",
     "• 10 models: User, Transaction,\n  Category, Budget, Tip, Insight,\n  Notification, Bookmark,\n  Announcement, PendingReg\n• Fallback: local → memory server", GREEN)
node(s, 9.6, 4.25, 3.18, 2.4, "SEEDS ON BOOT",
     "• 12 system categories\n• admin@campuscoin.app\n• demo@campuscoin.app\n• idempotent (skip if exists)", ROSE)

arrow(s, 4.12, 2.4, 0.7, 0.34)
arrow(s, 8.87, 2.4, 0.66, 0.34)
arrow(s, 4.12, 5.2, 0.7, 0.34, GREEN)
arrow(s, 8.87, 5.2, 0.66, 0.34, ROSE)

# ============================================================ 4 STRUCTURE
n += 1
s = slide(); header(s, "Project Structure"); footer(s, n, TOTAL)
box(s, 0.55, 1.35, 6.1, 5.5)
txt(s, 0.75, 1.5, 5.7, 0.35, "server/  — Express ESM API", 14, HONEY, True)
txt(s, 0.75, 1.9, 5.7, 4.9,
"""server/src/
├─ app.js  ·  server.js          boot + middleware stack
├─ config/    env · db · socket
├─ routes/    14 files → /api/v1/*
├─ controllers/ 11 *.controller.js
├─ models/    10 Mongoose schemas
├─ services/  tipsEngine · budgetAlerts
│              notify · ai/{categorize,
│              insight, chat, provider,
│              financeContext}
├─ middlewares/ protect · validate
│                rateLimit · error
├─ validators/  auth.validators (Zod)
├─ seeds/     categories · users · seed
└─ utils/     apiError · token · response""",
    11.5, MUTED, font="Consolas")
box(s, 6.9, 1.35, 5.88, 5.5)
txt(s, 7.1, 1.5, 5.5, 0.35, "client/  — Next.js 14 App Router", 14, BLUE, True)
txt(s, 7.1, 1.9, 5.5, 4.9,
"""client/src/
├─ app/
│  ├─ page.js               landing
│  ├─ (auth)/ login · register
│  │        forgot/reset-password
│  └─ (dashboard)/ dashboard,
│       transactions{,new,import,edit},
│       budgets · categories · reports,
│       tips · insights · bookmarks,
│       profile · admin{,users,
│       categories,announcements}
├─ components/ layout · ui · auth · ai
├─ store/  auth · ui · notifications
├─ hooks/  useSocket (WS singleton)
└─ lib/    api.js · utils · confetti""",
    11.5, MUTED, font="Consolas")

# ============================================================ 5 AUTH FLOW
n += 1
s = slide(); header(s, "Authentication Flow — OTP Register → JWT Session"); footer(s, n, TOTAL)
steps = [
    ("1", "REQUEST OTP", "POST /auth/request-otp\nname, email, password,\nacademicYear, savingsGoal\n→ bcrypt hash (cost 12)\n→ 6-digit OTP (sha256)\n→ PendingRegistration\n   TTL 10 min, 5 attempts\n→ devOtp returned in dev"),
    ("2", "VERIFY + CREATE", "POST /auth/register\nemail + otp\n→ check expiry/attempts\n→ User.create()\n→ seed 12 categories\n→ set cookies\n→ 201 + user + tokens"),
    ("3", "LOGIN", "POST /auth/login\n→ isActive check\n→ bcrypt compare\n→ loginStreak (days)\n→ cookies:\n  accessToken 15m  /\n  refreshToken 7d"),
    ("4", "REFRESH (auto)", "Any 401 in lib/api.js\n→ POST /auth/refresh\n  (refresh cookie only\n   scoped /auth path)\n→ re-issue both JWTs\n→ retry original request"),
]
x = 0.55
for i, (num, title, body) in enumerate(steps):
    box(s, x, 1.4, 3.0, 3.6, PANEL, LINE)
    chip(s, x + 0.15, 1.55, 0.4, 0.4, num, HONEY, RGBColor(0x1A, 0x12, 0x00), 13)
    txt(s, x + 0.65, 1.58, 2.2, 0.35, title, 12.5, HONEY, True)
    txt(s, x + 0.15, 2.1, 2.7, 2.8, body, 10.5, MUTED, font="Consolas")
    if i < 3:
        arrow(s, x + 3.05, 3.0, 0.35, 0.28)
    x += 3.35

box(s, 0.55, 5.25, 12.23, 1.55, PANEL2, LINE)
txt(s, 0.75, 5.38, 12, 0.3, "SECURITY DETAILS", 12, HONEY, True)
rich(s, 0.75, 5.7, 12, 1.0, [
    [("Cookies: ", 11.5, TEXT, True), ("httpOnly + sameSite=lax; access token path=/ (15 min), refresh path=/api/v1/auth (7 d) so it never leaks to other routes.", 11.5, MUTED, False)],
    [("Roles: ", 11.5, TEXT, True), ("JWT claim {sub, role, email} → protect middleware → adminOnly = requireRole('admin') guards ALL /admin routes. Client layout also redirects non-admins away from /admin*.", 11.5, MUTED, False)],
    [("Rate limits: ", 11.5, TEXT, True), ("authLimiter 30 req/15 min on auth endpoints · apiLimiter 500 req/15 min on /api · Zod validate() on every body · password reset = sha256 token, 30-min expiry.", 11.5, MUTED, False)],
])

# ============================================================ 6 AUTH UI
n += 1
s = slide(); header(s, "Auth Screens — Login & 3-Step OTP Registration"); footer(s, n, TOTAL)
pic(s, "02-login.png", 0.55, 1.4, 6.1)
pic(s, "03-register.png", 6.95, 1.4, 6.1)
txt(s, 0.55, 5.35, 6.1, 0.3, "Login — demo fill buttons, role-based redirect", 12, HONEY, True)
txt(s, 0.55, 5.68, 6.1, 1.1,
    "• Student → /dashboard · Admin → /admin\n• Show/hide password, ?next= deep link\n• Demo: admin@campuscoin.app / Admin@123\n• demo@campuscoin.app / Demo@123", 11.5, MUTED)
txt(s, 6.95, 5.35, 6.1, 0.3, "Register — wizard with 6-box OTP", 12, BLUE, True)
txt(s, 6.95, 5.68, 6.1, 1.1,
    "• Step 1 identity → Step 2 OTP → Step 3 money profile\n• Password strength meter + confetti\n• OTP shown as devOtp (no SMTP yet)\n• Optional: allowance, savings goal, currency", 11.5, MUTED)

# ============================================================ 7 REQUEST LIFECYCLE
n += 1
s = slide(); header(s, "API Request Lifecycle"); footer(s, n, TOTAL)
pipe = [
    ("HTTP Request", "fetch with\ncredentials:\n'include'"),
    ("CORS", "origin allowlist\nlocalhost:3000/3001\ncredentials:true"),
    ("helmet + JSON", "security headers\n1 MB body limit\ncookie-parser"),
    ("apiLimiter", "500 req / 15 min\n429 when exceeded"),
    ("/api/v1 router", "route file picks\nmethod + path"),
    ("validate(Zod)", "schema check →\n400 errors[] or\nreq.body replaced"),
    ("protect / adminOnly", "JWT from cookie\nor Bearer header\nreq.user set"),
    ("controller", "business logic →\nMongoose + services\n→ sendSuccess()"),
]
x = 0.4
for i, (t, b) in enumerate(pipe):
    accent = HONEY if i % 2 == 0 else BLUE
    box(s, x, 1.6, 1.5, 2.1, PANEL, LINE)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.6), Inches(1.5), Pt(3.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = accent; bar.line.fill.background(); bar.shadow.inherit = False
    txt(s, x + 0.07, 1.75, 1.36, 0.55, t, 10.5, accent, True, PP_ALIGN.CENTER)
    txt(s, x + 0.07, 2.35, 1.36, 1.25, b, 9.5, MUTED, align=PP_ALIGN.CENTER)
    if i < len(pipe) - 1:
        arrow(s, x + 1.52, 2.5, 0.18, 0.24)
    x += 1.62

box(s, 0.55, 4.1, 6.0, 2.7, PANEL2, LINE)
txt(s, 0.75, 4.25, 5.6, 0.3, "RESPONSE ENVELOPE (utils/response.js)", 12, GREEN, True)
txt(s, 0.75, 4.6, 5.6, 2.1,
"""success:  true | false
message:  "Logged in" | "Invalid email..."
data:     { user, accessToken, ... }
errors:   ["email: Required"]   (Zod)
stack:    shown only in development

// controller pattern
return sendSuccess(res, {…}, "OK");
throw ApiError.unauthorized("…");""", 11.5, MUTED, font="Consolas")

box(s, 6.78, 4.1, 6.0, 2.7, PANEL2, LINE)
txt(s, 6.98, 4.25, 5.6, 0.3, "ERROR HANDLER (middlewares/error.js)", 12, ROSE, True)
txt(s, 6.98, 4.6, 5.6, 2.1,
"""Mongoose ValidationError  → 400
CastError (bad ObjectId)  → 400
duplicate key 11000       → 409
ApiError.*                → its status
everything else           → 500

// notFound → 404 for unmatched
// logs stack unless NODE_ENV=test""", 11.5, MUTED, font="Consolas")

# ============================================================ 8 ROUTES MAP
n += 1
s = slide(); header(s, "Route Map — All Endpoints (/api/v1)"); footer(s, n, TOTAL)
rows = [
    ["Router", "Endpoints (method path)", "Guard"],
    ["auth", "POST request-otp · register · login · logout · refresh · forgot-password · reset-password · GET me", "public / protect"],
    ["users", "GET users · PATCH users · PATCH users/password", "protect"],
    ["categories", "GET · POST · PATCH :id · DELETE :id  (support ?type=income|expense)", "protect"],
    ["transactions", "GET list (filters+page) · POST · GET/:id · PATCH/:id · DELETE/:id · POST import", "protect"],
    ["budgets", "GET (?month) · POST upsert · DELETE :id", "protect"],
    ["dashboard", "GET dashboard  → one aggregated payload", "protect"],
    ["reports", "GET category · trend · daily-weekly · filtered", "protect"],
    ["tips", "GET list · POST refresh · PATCH :id/status", "protect"],
    ["bookmarks", "GET · POST toggle · DELETE :id", "protect"],
    ["notifications", "GET · PATCH read-all · PATCH :id/read", "protect"],
    ["admin", "GET stats/users/categories/announcements · CRUD users, system categories, announcements", "adminOnly"],
    ["ai", "GET status · insights · insight-stats/:month · POST categorize · categorize-batch · insight/:month · chat", "protect"],
    ["announcements", "GET /  (active, latest 10)", "public"],
]
table(s, 0.55, 1.35, 12.23, rows, col_w=[1.5, 8.7, 1.6], fsize=9.8, hsize=11, row_h=0.39, hrow_h=0.38)

# ============================================================ 9 CONTROLLERS 1
n += 1
s = slide(); header(s, "Controllers (1/2) — What Each One Does"); footer(s, n, TOTAL)
rows = [
    ["Controller", "Exported handlers", "Responsibility"],
    ["auth.controller", "requestOtp, register, login,\nlogout, refresh, me,\nforgotPassword, resetPassword", "OTP pending store, bcrypt verify,\nloginStreak, setAuthCookies\n(access 15m + refresh 7d),\nsha256 reset tokens"],
    ["user.controller", "getProfile, updateProfile,\nupdatePassword", "Whitelisted profile fields\n(name, year, allowance, goal,\ncurrency, theme, fontSize),\npassword change"],
    ["category.controller", "list, create, update, delete", "User + system defaults merge,\nduplicate-name 409, blocks\ndeleting category used by txs"],
    ["transaction.controller", "list, get, create, update,\ndelete, importTransactions", "Filters + pagination, AI auto-\ncategorize when no categoryId,\ncheckBudgetAlerts on expense,\ntx:created socket, bulk CSV"],
]
table(s, 0.55, 1.35, 12.23, rows, col_w=[2.1, 3.6, 6.5], fsize=10, hsize=11.5, row_h=1.15, hrow_h=0.4)
txt(s, 0.55, 6.45, 12.2, 0.5,
    "Pattern: every handler is asyncHandler-wrapped — thrown ApiError bubbles to errorHandler; responses always use sendSuccess/sendError envelope.",
    11.5, HONEY_L)

# ============================================================ 10 CONTROLLERS 2
n += 1
s = slide(); header(s, "Controllers (2/2) — Dashboard, Reports, Admin"); footer(s, n, TOTAL)
rows = [
    ["Controller", "Exported handlers", "Responsibility"],
    ["budget.controller", "listBudgets, upsertBudget,\ndeleteBudget", "Per (user, category, month) upsert,\nspent% aggregation, budget:updated\nsocket, notifications"],
    ["dashboard.controller", "getDashboard", "Single Promise.all aggregation:\nincome/expense/balance, topCategory,\nrecent tx, pinned tips, unread notifs,\nbudgets w/ %, 180-day trend"],
    ["report.controller", "categoryReport, sixMonthTrend,\ndailyWeeklySummary, filteredReport", "Donut data, 6-month line, daily +\nISO-week bars, arbitrary filter →\nbyCategory + totals + transactions"],
    ["tip.controller / bookmark\n/ notification", "list, refresh, status; toggle;\nlist, markRead, markAllRead", "tipsEngine.generateTips() recompute,\npin/dismiss, bookmark toggle\n(Tip|Insight), unread count"],
    ["admin.controller", "getStats, listUsers, toggle,\nresetPwd, deleteUser, CRUD\ndefault categories + announcements", "Platform stats + top categories,\nuser search/disable/delete,\nsystem category CRUD,\nannouncement broadcast"],
]
table(s, 0.55, 1.35, 12.23, rows, col_w=[2.3, 3.7, 6.2], fsize=10, hsize=11.5, row_h=1.0, hrow_h=0.4)

# ============================================================ 11 MODELS
n += 1
s = slide(); header(s, "Data Model — 10 Mongoose Schemas"); footer(s, n, TOTAL)
rows = [
    ["Model", "Key fields", "Indexes / notes"],
    ["User", "name, email(uniq), password(bcrypt 12), role student|admin,\nacademicYear, allowanceBaseline, savingsGoal, currency, theme,\nfontSize, isActive, loginStreak, lastLoginAt", "email unique;\ntoSafeJSON() hides password"],
    ["PendingRegistration", "profile copy + otpHash(sha256), otpExpires, attempts", "TTL index on otpExpires\n(auto-purge 10 min)"],
    ["Category", "userId(null=system), name, type income|expense,\nicon, color, isDefault", "(userId,type), (userId,name,type)"],
    ["Transaction", "userId, type, amount≥0.01, categoryId, note, date,\nisRecurring, recurringDay 1–31, aiSuggested,\nuserCorrectedCategory, flags[]", "(userId,date),\n(userId,categoryId,date)"],
    ["Budget", "userId, categoryId, month YYYY-MM, limit≥0", "UNIQUE (userId,categoryId,month)"],
    ["Tip / Insight / Bookmark", "Tip: title, body, impactScore, status\nInsight: month, narrative, flags, meta (AI cache)\nBookmark: refModel Tip|Insight, refId, title, snippet", "Insight UNIQUE (user, month)\nBookmark UNIQUE (user, ref)"],
    ["Notification / Announcement", "Notification: userId, type enum, title, message, read\nAnnouncement: title, body, active (global)", "(userId, read, createdAt)"],
]
table(s, 0.55, 1.3, 12.23, rows, col_w=[2.4, 6.6, 3.2], fsize=9.6, hsize=11, row_h=0.72, hrow_h=0.36)

# ============================================================ 12 SERVICES
n += 1
s = slide(); header(s, "Server Services — Tips Engine, Budget Alerts, Notify"); footer(s, n, TOTAL)
box(s, 0.55, 1.4, 4.0, 5.35, PANEL, LINE)
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(1.4), Inches(4.0), Pt(4))
bar.fill.solid(); bar.fill.fore_color.rgb = HONEY; bar.line.fill.background(); bar.shadow.inherit = False
txt(s, 0.75, 1.55, 3.6, 0.35, "💡 tipsEngine.js", 14, HONEY, True)
txt(s, 0.75, 1.95, 3.6, 4.7,
"""generateTips(userId) compares
this month vs last month:

• Category spend up >20%
  → "Food spending up 40%"
    impact = rise % (cap 100)
• Top spend category
  → impact = min(90, total/100)
• Budget >70% used
  → impact 85
• Savings rate <20% (3 mo)
  → impact 95

Ranked by impactScore, top 6
upserted by (userId, title);
pinned/dismissed never overwritten
→ GET /tips · POST /tips/refresh""", 11, MUTED, font="Consolas")

box(s, 4.75, 1.4, 4.0, 5.35, PANEL, LINE)
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.75), Inches(1.4), Inches(4.0), Pt(4))
bar.fill.solid(); bar.fill.fore_color.rgb = ROSE; bar.line.fill.background(); bar.shadow.inherit = False
txt(s, 4.95, 1.55, 3.6, 0.35, "🔔 budgetAlerts.js", 14, ROSE, True)
txt(s, 4.95, 1.95, 3.6, 4.7,
"""checkBudgetAlerts(user, cat, date)
runs after every expense create/
update/import:

• find budget (cat + month)
• aggregate month-to-date spend
• pct = spent / limit
• emit budget:updated (socket)

pct ≥ 100 → 'Budget exceeded'
  level: exceeded (deduped)
pct ≥ 80  → 'Budget warning'
  level: warning (regex dedup)

Never throws — logs + returns []
→ fires Notification + toast/badge""", 11, MUTED, font="Consolas")

box(s, 8.95, 1.4, 3.83, 5.35, PANEL, LINE)
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.95), Inches(1.4), Inches(3.83), Pt(4))
bar.fill.solid(); bar.fill.fore_color.rgb = GREEN; bar.line.fill.background(); bar.shadow.inherit = False
txt(s, 9.15, 1.55, 3.5, 0.35, "📡 notify.js + socket", 14, GREEN, True)
txt(s, 9.15, 1.95, 3.45, 4.7,
"""notifyUser(id, {type, title,
message}):
  → Notification.create
  → emit notification:new
     to room user:{id}

broadcastNotification(…):
  → insertMany for every
    active user
  → emit to each room
  → emitToAll
    announcement:new

socket.js:
  handshake must carry valid
  access JWT, else Unauthorized
  join user:{userId} room""", 11, MUTED, font="Consolas")

# ============================================================ 13 AI
n += 1
s = slide(); header(s, "AI Layer — Categorize · Insights · BudgetBee Chat"); footer(s, n, TOTAL)
box(s, 0.55, 1.4, 4.0, 2.55, PANEL, LINE)
txt(s, 0.75, 1.55, 3.6, 0.35, "🏷  aiCategorize", 13.5, HONEY, True)
txt(s, 0.75, 1.95, 3.6, 1.9,
"""Typing a note on New Transaction
→ debounced POST /ai/categorize
→ LLM constrained to your real
   category names (temp 0.1, 8s)
→ fallback: 10 keyword rules
   (cafe→Food, uber→Transport…)
→ badge "AI suggested"; manual
   edit clears the flag""", 10.8, MUTED)

box(s, 0.55, 4.15, 4.0, 2.6, PANEL, LINE)
txt(s, 0.75, 4.3, 3.6, 0.35, "📊  aiInsight", 13.5, BLUE, True)
txt(s, 0.75, 4.7, 3.6, 1.95,
"""buildMonthStats() → income,
expense, byCategory, flags
(rises >20%, budget exceeded)
→ LLM 3–5 sentence narrative
→ rule-template fallback
→ cached in Insight (user,month)
→ GET /ai/insights = 12-mo
   history on Insights page""", 10.8, MUTED)

box(s, 4.75, 1.4, 4.0, 5.35, PANEL, LINE)
txt(s, 4.95, 1.55, 3.6, 0.35, "🐝  BudgetBee Chat", 13.5, GREEN, True)
txt(s, 4.95, 1.95, 3.6, 4.7,
"""Floating widget (students only)
POST /ai/chat {message, history}

Resolution order:
1) financial intent?
   buildFinanceContext():
   safe-to-spend, daily burn,
   budget rows, goal progress
   → rule verdict FIRST
     (buy/wait/not this month)
   → LLM polishes (fallback: rules)
2) FAQ matcher (9 entries)
3) general LLM + month stats
4) static help text

History in localStorage,
source badge on each reply""", 10.8, MUTED, font="Consolas")

box(s, 8.95, 1.4, 3.83, 5.35, PANEL, LINE)
txt(s, 9.15, 1.55, 3.5, 0.35, "🔌  provider.js", 13.5, ROSE, True)
txt(s, 9.15, 1.95, 3.45, 4.7,
"""llmChat(messages, opts):

 1. Groq
    llama-3.3-70b-versatile
    (GROQ_API_KEY)
 2. OpenRouter
    claude-3.5-haiku
    (OPENROUTER_API_KEY)
 3. throw → callers use rules

Status: GET /ai/status →
 {groq, openrouter, mode}

Current .env has no keys
→ runs rules-only, no crash""", 10.8, MUTED, font="Consolas")

# ============================================================ 14 SOCKET
n += 1
s = slide(); header(s, "Realtime — Socket.IO Event Flow"); footer(s, n, TOTAL)
box(s, 0.55, 1.45, 5.6, 5.3, PANEL, LINE)
txt(s, 0.75, 1.6, 5.2, 0.35, "SERVER  →  CLIENT events", 14, HONEY, True)
rows = [
    ["Event", "Emitted from", "Payload"],
    ["notification:new", "notifyUser / broadcast", "Notification doc"],
    ["budget:updated", "budgetAlerts · budget ctrl", "{catId, month,\nspent, limit, %}"],
    ["announcement:new", "broadcastNotification", "{title, message}"],
    ["tx:created", "createTransaction", "{id}"],
]
table(s, 0.75, 2.1, 5.2, rows, col_w=[2.0, 2.0, 1.6], fsize=10, hsize=10.5, row_h=0.6, hrow_h=0.36)
txt(s, 0.75, 4.9, 5.2, 1.7,
"""Handshake auth: socket.auth.token
= accessToken (store / sessionStorage)
Invalid → connection rejected.

Rooms: user:{userId} — emitToUser
targets only that user's sockets.
connect() only when logged in.""", 11, MUTED)

box(s, 6.4, 1.45, 6.38, 5.3, PANEL, LINE)
txt(s, 6.6, 1.6, 6.0, 0.35, "CLIENT  —  useSocket() + stores", 14, BLUE, True)
txt(s, 6.6, 2.05, 6.0, 4.5,
"""hooks/useSocket.js
• singleton io(NEXT_PUBLIC_WS_URL)
• connects after login with JWT
• on notification:new →
    notificationStore.pushLive(n)
    + Toaster toast (warning if
      type == budget_alert)
• on announcement:new → reload
    announcement banner
• returns { connected, on, socket }

Topbar live dot = connected state
(breathing emerald indicator)

Notifications store: items (cap 50),
unread badge, mark-all-read API,
60s poll fallback + WS refresh.""", 11, MUTED, font="Consolas")

# ============================================================ 15 CLIENT PAGES
n += 1
s = slide(); header(s, "Client Pages — Full Route Map"); footer(s, n, TOTAL)
rows = [
    ["Route", "Page", "What it does"],
    ["/", "Landing", "Marketing hero, features, testimonials, visual sitemap tree"],
    ["/login · /register · /forgot · /reset", "Auth", "OTP wizard, strength meter, dev reset link on screen"],
    ["/dashboard", "Home", "Greeting, balance/income/expense cards, budgets vs actual,\nrecent tx, pinned tips, streak, announcements, confetti on goal"],
    ["/transactions · /new · /import · /[id]/edit", "Transactions", "Filterable list; AI live category suggest; CSV map→categorize→import"],
    ["/budgets · /categories", "Money", "Progress bars + month picker; personal + system categories CRUD"],
    ["/reports", "Reports", "Recharts donut + 6-month line + daily/weekly bars + PDF export"],
    ["/tips · /insights · /bookmarks", "AI & saving", "Pin/dismiss tips; monthly narrative + history; saved items"],
    ["/profile", "Account", "Edit profile, currency, change password, logout"],
    ["/admin · /users · /categories · /announcements", "Admin", "Stats, user management, system categories, broadcast announcements"],
]
table(s, 0.55, 1.35, 12.23, rows, col_w=[3.4, 1.7, 7.1], fsize=10, hsize=11.5, row_h=0.55, hrow_h=0.38)

# ============================================================ 16 DASHBOARD
n += 1
s = slide(); header(s, "Dashboard — Student Home"); footer(s, n, TOTAL)
pic(s, "06-dashboard.png", 0.55, 1.35, 8.1)
box(s, 8.9, 1.35, 3.88, 5.35)
txt(s, 9.1, 1.5, 3.5, 0.3, "BUILT FROM ONE API CALL", 11, HONEY, True)
txt(s, 9.1, 1.85, 3.5, 4.7,
"""GET /dashboard returns:

• time-based greeting
• balance / income / expense
• top expense category
• 6 recent transactions
• 3 pinned tips
• 10 unread notifications
• budgets + spent %
• 180-day income/expense trend

UI extras:
• login streak badge 🔥
• announcement banner
• confetti when savings goal
  is reached
• quick-add action cards""", 11, MUTED)

# ============================================================ 17 TRANSACTIONS
n += 1
s = slide(); header(s, "Transactions — List, AI Quick-Add, CSV Import"); footer(s, n, TOTAL)
pic(s, "07-transactions.png", 0.4, 1.35, 6.25)
pic(s, "08-new-transaction.png", 6.85, 1.35, 6.25)
txt(s, 0.4, 5.35, 6.2, 0.3, "List — filters, pagination, edit/delete", 12, HONEY, True)
txt(s, 0.4, 5.68, 6.2, 1.2,
"• type / category / date-range / text search\n• recurring badge, populated category chip\n• confirm dialogs on delete\n• PATCH /transactions/:id clears aiSuggested on manual category change", 11, MUTED)
txt(s, 6.85, 5.35, 6.2, 0.3, "New — live AI category suggestion", 12, BLUE, True)
txt(s, 6.85, 5.68, 6.2, 1.2,
"• type a note → debounced POST /ai/categorize\n• honey badge: “AI suggested”\n• recurring toggle + day of month (1–31)\n• expense triggers budget alert check + socket", 11, MUTED)

# ============================================================ 18 BUDGETS + REPORTS
n += 1
s = slide(); header(s, "Budgets & Reports"); footer(s, n, TOTAL)
pic(s, "09-budgets.png", 0.4, 1.35, 6.25)
pic(s, "10-reports.png", 6.85, 1.35, 6.25)
txt(s, 0.4, 5.35, 6.2, 0.3, "Budgets — category limits per month", 12, HONEY, True)
txt(s, 0.4, 5.68, 6.2, 1.2,
"• unique (user, category, month) upsert\n• progress bars: green → honey → rose at 80/100%\n• live % updates via budget:updated socket\n• confetti when all budgets stay safe", 11, MUTED)
txt(s, 6.85, 5.35, 6.2, 0.3, "Reports — charts + PDF export", 12, GREEN, True)
txt(s, 6.85, 5.68, 6.2, 1.2,
"• donut: category-wise expense for a month\n• line: 6-month income vs expense trend\n• bars: daily + weekly summary\n• Export PDF = html2canvas → jsPDF (client-side)", 11, MUTED)

# ============================================================ 19 TIPS + INSIGHTS
n += 1
s = slide(); header(s, "Saving Tips & AI Insights"); footer(s, n, TOTAL)
pic(s, "11-tips.png", 0.4, 1.35, 6.25)
pic(s, "12-insights.png", 6.85, 1.35, 6.25)
txt(s, 0.4, 5.35, 6.2, 0.3, "Tips — ranked by impact", 12, HONEY, True)
txt(s, 0.4, 5.68, 6.2, 1.2,
"• rule engine compares vs last month\n• pin / dismiss / bookmark each tip\n• “Refresh tips” re-runs the engine\n• impactScore sorts the list", 11, MUTED)
txt(s, 6.85, 5.35, 6.2, 0.3, "Insights — monthly narrative", 12, BLUE, True)
txt(s, 6.85, 5.68, 6.2, 1.2,
"• warm 3–5 sentence story of your month\n• flags: “Food rose 40%”, “budget exceeded”\n• month picker + 12-month history\n• regenerate button (force=true)", 11, MUTED)

# ============================================================ 20 CSV + CATEGORIES
n += 1
s = slide(); header(s, "CSV Import & Category Management"); footer(s, n, TOTAL)
pic(s, "14-csv-import.png", 0.4, 1.35, 6.25)
pic(s, "13-categories.png", 6.85, 1.35, 6.25)
txt(s, 0.4, 5.35, 6.2, 0.3, "CSV Import — PapaParse pipeline", 12, HONEY, True)
txt(s, 0.4, 5.68, 6.2, 1.2,
"• upload → map columns → preview table\n• “AI categorize” = POST /ai/categorize-batch (≤100 rows)\n• confirm → POST /transactions/import (≤500 rows)\n• notification reports imported + skipped counts", 11, MUTED)
txt(s, 6.85, 5.35, 6.2, 0.3, "Categories — personal + system defaults", 12, ROSE, True)
txt(s, 6.85, 5.68, 6.2, 1.2,
"• 12 seeded defaults (5 income / 7 expense)\n• add custom, edit colors/icons, type filter\n• delete blocked if transactions reference it\n• admins manage system defaults at /admin/categories", 11, MUTED)

# ============================================================ 21 ADMIN
n += 1
s = slide(); header(s, "Admin Panel", kicker="CAMPUS COIN · ROLE: ADMIN"); footer(s, n, TOTAL)
pic(s, "04-admin.png", 0.4, 1.35, 6.25)
pic(s, "05-admin-users.png", 6.85, 1.35, 6.25)
txt(s, 0.4, 5.35, 6.2, 0.3, "Overview — /admin", 12, ROSE, True)
txt(s, 0.4, 5.68, 6.2, 1.2,
"• users / transactions / categories counts\n• 7-day active users, top-5 expense categories\n• AI provider status (groq / openrouter / rules)\n• recent announcements", 11, MUTED)
txt(s, 6.85, 5.35, 6.2, 0.3, "Users — /admin/users", 12, HONEY, True)
txt(s, 6.85, 5.68, 6.2, 1.2,
"• search by name/email, pagination\n• enable / disable account (isActive)\n• reset password (default Reset@123)\n• delete non-admin users · AdminSidebar layout", 11, MUTED)

# ============================================================ 22 FEATURES T1
n += 1
s = slide(); header(s, "Features — Tier 1 Core (20/20)"); footer(s, n, TOTAL)
col1 = [
    "1  Register (OTP, profile, goal)",
    "2  Login — student + admin",
    "3  Secure sessions (JWT cookies)",
    "4  Password recovery / reset",
    "5  Editable user profile",
    "6  Category management (12 seeds)",
    "7  Transaction CRUD + filters",
    "8  Recurring flag (day 1–31)*",
    "9  Dashboard (balance, widgets)",
    "10  Monthly reports (3 chart types)",
]
col2 = [
    "11  Export PDF / image (jsPDF)",
    "12  Budget goals per category",
    "13  Budget alerts 80% / 100%",
    "14  Saving-tips engine (impact rank)",
    "15  Bookmark tips & insights",
    "16  Admin panel (stats, users, CMS)",
    "17  Dark mode + font-size toggle",
    "18  Breadcrumbs on every page",
    "19  Visual sitemap on homepage",
    "20  Fully responsive (drawer sidebar)",
]
box(s, 0.55, 1.4, 6.0, 4.6, PANEL, LINE)
bullets(s, 0.75, 1.6, 5.6, 4.3, col1, 12.5)
box(s, 6.78, 1.4, 6.0, 4.6, PANEL, LINE)
bullets(s, 6.98, 1.6, 5.6, 4.3, col2, 12.5)
box(s, 0.55, 6.15, 12.23, 0.72, PANEL2, LINE)
txt(s, 0.75, 6.28, 12, 0.5,
    "* Recurring is stored & toggleable in the form; no cron clones it monthly yet.  All other Tier-1 features are fully wired end-to-end (API + UI).",
    11.5, HONEY_L)

# ============================================================ 23 FEATURES T2/3
n += 1
s = slide(); header(s, "Features — Tier 2 Wow & Tier 3 Extras"); footer(s, n, TOTAL)
rows = [
    ["#", "Feature", "Status", "How"],
    ["21", "AI expense categorization", "✅", "LLM + keyword rules, live suggest, badge"],
    ["22", "AI monthly insights", "✅", "Cached Insight narrative + flags"],
    ["23", "CSV import w/ batch AI", "✅", "PapaParse → categorize-batch → bulk insert"],
    ["24", "Next-month forecast", "⚡", "projectedEomExpense inside chat answers"],
    ["25", "Duplicate / large detect", "—", "flags[] in schema, writer not implemented"],
    ["27 / 28 / 29", "Pin-dismiss tips · insight history · PDF", "✅", "All live"],
    ["31", "AI chatbot BudgetBee", "✅", "Context advisor + FAQ + LLM fallback"],
    ["32 / 33 / 34", "Animated charts · confetti · streak", "✅", "Recharts/Framer · celebrate() · loginStreak"],
    ["39", "Multi-currency", "⚡", "BDT/USD/EUR/… display + symbols (no FX)"],
]
table(s, 0.55, 1.4, 12.23, rows, col_w=[1.3, 3.6, 1.0, 6.3], fsize=11, hsize=11.5, row_h=0.5, hrow_h=0.4)
box(s, 0.55, 6.15, 12.23, 0.72, PANEL2, LINE)
txt(s, 0.75, 6.28, 12, 0.5,
    "Tier-3 extras not built: PWA, voice input, receipt OCR, auto light/dark by time, gamification badges.  AI works rules-only until GROQ_API_KEY / OPENROUTER_API_KEY is added.",
    11.5, MUTED)

# ============================================================ 24 RUN
n += 1
s = slide(); header(s, "How to Run — Commands, Ports, Environment"); footer(s, n, TOTAL)
box(s, 0.55, 1.4, 6.0, 3.4, PANEL, LINE)
txt(s, 0.75, 1.55, 5.6, 0.3, "START (two terminals)", 13, HONEY, True)
txt(s, 0.75, 1.95, 5.6, 2.8,
"""# API — port 5000
cd server
npm install
npm run dev          # node --watch
# npm run seed       # optional (runs on boot)

# Client — port 3000
cd client
npm install
npm run dev          # next dev

# checks
GET :5000/api/v1/health → 200
UI  :3000 → landing page""", 11.5, MUTED, font="Consolas")

box(s, 6.78, 1.4, 6.0, 3.4, PANEL, LINE)
txt(s, 6.98, 1.55, 5.6, 0.3, "ENV (server/.env)", 13, BLUE, True)
txt(s, 6.98, 1.95, 5.6, 2.8,
"""PORT=5000
NODE_ENV=development
CLIENT_URL=http://localhost:3000

MONGODB_URI=mongodb+srv://…Atlas…
TRY_ATLAS_FIRST=true     → Atlas first,
  local → mongodb-memory-server fallback

JWT_ACCESS_SECRET=…   JWT_REFRESH_SECRET=…
GROQ_API_KEY=…   OPENROUTER_API_KEY=…

client/.env.local:
NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
NEXT_PUBLIC_WS_URL=http://localhost:5000""", 11, MUTED, font="Consolas")

box(s, 0.55, 5.0, 12.23, 1.85, PANEL2, LINE)
txt(s, 0.75, 5.15, 12, 0.3, "DEMO ACCOUNTS (seeded on every boot)", 13, GREEN, True)
rich(s, 0.75, 5.55, 12, 1.2, [
    [("🐝  Admin:  ", 14, HONEY, True), ("admin@campuscoin.app   /   Admin@123", 14, TEXT, True), ("     → lands on /admin", 12, MUTED, False)],
    [("🎓  Student:  ", 14, BLUE, True), ("demo@campuscoin.app   /   Demo@123", 14, TEXT, True), ("     → lands on /dashboard", 12, MUTED, False)],
    [("Login page has one-click demo fill buttons.  Data persists in MongoDB Atlas (cluster0.wyyaakz).", 11.5, MUTED, False)],
])

# ============================================================ 26 END
n += 1
s = slide()
blk = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.35), prs.slide_height)
blk.fill.solid(); blk.fill.fore_color.rgb = HONEY; blk.line.fill.background(); blk.shadow.inherit = False
txt(s, 1.0, 1.9, 11.5, 1.0, "Thank You", 52, TEXT, True)
chip(s, 1.0, 3.0, 2.5, 0.44, "TEAM BOMBERS", HONEY, RGBColor(0x1A, 0x12, 0x00), 13)
txt(s, 3.7, 3.04, 8.5, 0.4, "Bilawal · Owais · Esam · Muneeb · Haider", 15, TEXT, True)
txt(s, 1.0, 3.7, 11.5, 0.6, "Campus Coin — NextGen BudgetBee is ready to demo", 20, HONEY_L, True)
txt(s, 1.0, 4.4, 11, 1.3,
"""This deck covered: architecture · every route · all 11 controllers · 10 models · services (tips, alerts, notify) ·
AI layer (categorize / insights / chat) · Socket.IO realtime · 21 client pages · auth (OTP + JWT) ·
Tier 1/2/3 feature status · run instructions.   Questions?""", 13.5, MUTED)
chip(s, 1.0, 6.1, 3.4, 0.44, "UI  http://localhost:3000", PANEL2, HONEY_L, 12)
chip(s, 4.6, 6.1, 3.4, 0.44, "API  http://localhost:5000", PANEL2, HONEY_L, 12)
chip(s, 8.2, 6.1, 4.3, 0.44, "github.com/owais2507d-alt/MAlik_Owais_Campus_Coim", PANEL2, HONEY_L, 10.5)
footer(s, n, TOTAL)

prs.save(OUT)
print("SAVED", OUT, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
