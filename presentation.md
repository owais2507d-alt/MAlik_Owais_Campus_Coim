# Campus Coin — Team Bombers
## Project Presentation (PowerPoint Source)

> **How to use:** each numbered section = one slide. Follow the *Layout* line to place
> text/images in PowerPoint. Brand palette: background `#0C0C10`, panels `#17171E`,
> accent honey `#F59E0B`, text white `#FAFAFA`, muted `#A1A1AA`.
> Screenshots live in `ppt/screenshots/` (14 shots, 1440×900).
> Auto-generate deck: `python ppt/build_pptx.py` → `Campus-Coin-Project.pptx`.

---

## Slide 1 — Title
**Layout:** full dark background, thin honey bar on the left edge, centered text.

- **CAMPUS COIN**
- *NextGen BudgetBee — Smart Budget Tracker for Students*
- **Team Bombers**
- Muhammad Bilawal · Muhammad Owais · Muhammad Esam · Muhammad Muneeb · Syed Haider
- Footer: `Client :3000 · API :5000 · MongoDB Atlas`

---

## Slide 2 — Meet the Team
**Layout:** 5 cards in a row (rounded rectangles, honey top-border), name + role under each.

| Member | Role |
|---|---|
| **Muhammad Bilawal** | Project lead · Backend & database |
| **Muhammad Owais** | Full-stack · Auth, admin & deployment |
| **Muhammad Esam** | AI features · Tips & insights engine |
| **Muhammad Muneeb** | Frontend · Dashboard & reports UI |
| **Syed Haider** | Testing · E2E suite & documentation |

*(Adjust roles to match actual work — this line keeps every slide in sync.)*

---

## Slide 3 — Agenda
**Layout:** two columns of numbered chips.

1. Problem we solve
2. Solution & demo highlights
3. Tech stack & architecture
4. Authentication & security
5. Feature tour (screenshots)
6. AI layer (BudgetBee)
7. Realtime alerts
8. Database & API
9. Testing & deployment
10. Future scope · Q&A

---

## Slide 4 — The Problem
**Layout:** left = big statement, right = 4 icon bullets.

- Students have **money but no system** — cash, bKash, hostel meals, chai, exams
- Expenses tracked in notebooks or **never** → overspending before month-end
- Generic finance apps feel **too corporate** — no student categories, no BD context
- Budgets fail because they're **boring and invisible** until it's too late

---

## Slide 5 — Our Solution
**Layout:** screenshot left (01-landing.png), bullets right.

**Campus Coin** — a fast, mobile-first budget tracker built *for students*:

- Log income/expense in **&lt; 5 seconds** with AI auto-category
- Per-category **monthly budgets** with live 80% / 100% alerts
- **Saving tips** ranked by impact + monthly AI insights
- **BudgetBee chat** — “can I afford a 400 Taka dinner?” → instant answer
- Reports + **PDF export**, CSV import, streaks, dark mode

---

## Slide 6 — Tech Stack
**Layout:** 3 grouped chip rows.

- **Frontend:** Next.js 14 (App Router) · React 18 · Tailwind CSS 3 · Zustand · Recharts · Framer Motion
- **Backend:** Express 4 (ESM, MVC) · Mongoose 8 · Zod validation · Socket.IO 4 · JWT (access+refresh)
- **Platform:** MongoDB Atlas · Groq LLM (`gpt-oss-120b`) with rule-based fallback · nodemailer SMTP · ngrok tunnel · GitHub

---

## Slide 7 — Architecture
**Layout:** diagram (boxes + arrows).

```
Browser (Next.js :3000)
   │  fetch /api/v1  (same-origin → Next rewrite proxy)
   ▼
Express API (:5000)  ──►  routes → Zod validate → protect/adminOnly
   │                        → controllers → services → Mongoose
   ├────────► MongoDB Atlas (10 models)
   ├────────► Socket.IO (rooms: user:{id})
   └────────► Groq LLM  ──fallback──►  keyword rules
```

*Note: single-tunnel design lets the whole app run behind one ngrok URL.*

---

## Slide 8 — Authentication Flow
**Layout:** 4 step cards left→right with arrows.

1. **Request OTP** — bcrypt(12) hash, 6-digit code, 10-min TTL, 5 attempts
2. **Register** — verify OTP → account + welcome data
3. **Login** — access JWT 15 min + refresh JWT 7 days (httpOnly cookies)
4. **Auto-refresh** — any 401 → silent refresh → retry (zero re-login)

Guards: `protect` (student) · `adminOnly` (admin) · rate-limited (30 req/15 min) · role-aware routes

---

## Slide 9 — Feature Tour: Dashboard
**Layout:** full-width screenshot `ppt/screenshots/06-dashboard.png`, caption strip below.

- Balance / income / expense cards · top category · recent transactions
- Budgets vs actual with progress bars · pinned tips · login streak 🔥
- Announcement banner · savings-goal confetti

---

## Slide 10 — Feature Tour: Transactions & CSV
**Layout:** two screenshots side-by-side: `07-transactions.png` + `08-new-transaction.png`.

- Filters: type, category, date range, text search · pagination
- **New transaction:** type a note → AI suggests category live (badge "AI suggested")
- Recurring flag with day-of-month · edit/delete with confirm
- **CSV import** (`14-csv-import.png`): map columns → AI batch-categorize → bulk insert

---

## Slide 11 — Feature Tour: Budgets & Reports
**Layout:** two screenshots: `09-budgets.png` + `10-reports.png`.

- Budgets: one limit per category/month, progress color green → honey → rose at 80/100%
- Live updates over WebSocket — bar animates as you spend
- Reports: category donut · 6-month income/expense trend · daily & weekly bars
- **Export PDF** client-side (html2canvas + jsPDF)

---

## Slide 12 — Feature Tour: Tips, Insights, Categories
**Layout:** three small screenshots: `11-tips.png`, `12-insights.png`, `13-categories.png`.

- **Tips:** engine compares this month vs last → impact-ranked advice; pin / dismiss / bookmark
- **Insights:** warm 3–5 sentence monthly story + flags (“Food rose 40%”)
- **Categories:** 12 system defaults + personal custom, search & source filter

---

## Slide 13 — AI Layer (BudgetBee)
**Layout:** left column chat screenshot/diagram, right column provider chain.

- **Categorize** — LLM constrained to your real category names (temp 0.1) + per-user learning
- **Insights** — month stats → narrative, cached per (user, month)
- **Chat advisor** — safe-to-spend, daily burn, budget verdicts; FAQ + smalltalk
- **Provider chain:** Groq → OpenRouter → local rules (works with **no keys**, demo-safe)
- Markdown stripped for clean bubbles · friendly error messages

---

## Slide 14 — Realtime Notifications
**Layout:** event-flow diagram (server → socket → phone toast).

- Events: `notification:new` · `budget:updated` · `announcement:new` · `tx:created`
- JWT handshake → auto-join `user:{id}` room
- Topbar live dot · unread badge · 60 s poll fallback
- Admin **broadcast announcement** reaches every student instantly

---

## Slide 15 — Database Design
**Layout:** grid of 4×3 model cards (name + 2 key fields).

- **User** — email, bcrypt password, role, streak, currency
- **Transaction** — amount, type, category ref, date, recurring, AI flags
- **Budget** — UNIQUE(user, category, month) · spent %
- **Category** — system (`userId:null`) vs personal
- **Tip / Insight / Bookmark** — advice, cached narratives, saved items
- **Notification / Announcement / PendingRegistration / OTP TTL index**

---

## Slide 16 — API at a Glance
**Layout:** table.

| Area | Endpoints | Guard |
|---|---|---|
| auth | request-otp · register · login · refresh · forgot/reset | public |
| transactions | list · create · update · delete · import | protect |
| budgets / reports / tips | upsert · charts · refresh | protect |
| dashboard / ai | aggregated · categorize · insights · chat | protect |
| admin | stats · users · categories · announcements | adminOnly |
| announcements | active list | public |

Envelope: `{ success, message, data }` · errors via `ApiError` · Zod on every body

---

## Slide 17 — Testing & Quality
**Layout:** checklist rows with green ticks.

- ✅ **Playwright E2E suite** (`e2e/run_e2e.py`) — reads OTP from dev log
- ✅ Requirement coverage report (`extras/req-coverage-report.md`)
- ✅ Manual edge fixes: amount cap 10M, budget min 1, delete rules, search filters
- ✅ Build gates: `client lint → build` · server boot + `/api/v1/health`
- ✅ Works offline to AI: rule fallback keeps every feature demo-safe

---

## Slide 18 — Deployment & DevOps
**Layout:** two cards — Local / Cloud.

**Local dev**
- `server npm run dev` (:5000) + `client npm run dev` (:3000)
- Single-tunnel ngrok for mobile testing (rewrites proxy API + sockets)

**Production ready**
- `render.yaml` blueprint · `API_PROXY_URL` parameterized
- SMTP OTP + password-reset emails (Gmail app password verified)
- Refuses silent in-memory DB fallback in production

---

## Slide 19 — Project Structure
**Layout:** two code trees (monospace, small font).

```
server/src/                 client/src/
├─ routes/    (14 files)    ├─ app/(auth)  login·register·reset
├─ controllers/ (11)        ├─ app/(dashboard) 18 pages
├─ models/    (10)          ├─ components/ ui·layout·ai
├─ services/  tips·budgets  ├─ store/ auth·ui·notifications
│   ·notify·ai/{categorize, ├─ hooks/ useSocket
│   insight,chat,provider}  └─ lib/ api.js (401 auto-refresh)
└─ seeds/ · middlewares/ · validators/
```

---

## Slide 20 — Future Scope
**Layout:** 5 chips.

- 🔁 Recurring auto-copy cron (schema ready)
- 🧾 Receipt OCR & duplicate detection
- 📱 PWA install + offline queue
- 🏆 Gamification badges & leaderboards
- 🌍 Multi-currency with live FX rates

---

## Slide 21 — Thank You
**Layout:** title style like Slide 1.

- **Thank You — Team Bombers**
- *Campus Coin: NextGen BudgetBee*
- Live demo link / GitHub: `github.com/owais2507d-alt/MAlik_Owais_Campus_Coim`
- **Q&A**

---

### Designer notes (keep slides “looking good”)

- **One idea per slide** — max 5 bullets, ≤ 10 words each
- **Show, don't tell:** any slide about a feature should embed its screenshot
- Dark theme + honey accent everywhere; never mix more than 3 colors per slide
- Tables for API/data; diagrams for flows; cards for people/features
- Font: **Segoe UI** (titles 26–54 pt bold, body 11–14 pt)
