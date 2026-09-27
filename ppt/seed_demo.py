import json
import random
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError

API = "http://localhost:5000/api/v1"

def req(method, path, body=None, token=None):
    data = json.dumps(body).encode() if body is not None else None
    r = Request(f"{API}{path}", data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if token:
        r.add_header("Authorization", f"Bearer {token}")
    try:
        with urlopen(r) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        print(method, path, e.code, e.read().decode()[:200])
        raise

# login
login = req("POST", "/auth/login", {"email": "demo@campuscoin.app", "password": "Demo@123"})
tok = login["data"]["accessToken"]
print("logged in")

cats = req("GET", "/categories", token=tok)["data"]["categories"]
income_cats = [c for c in cats if c["type"] == "income"]
expense_cats = [c for c in cats if c["type"] == "expense"]
print(f"categories: {len(cats)}")

# check if already has data
existing = req("GET", "/transactions?limit=1", token=tok)["data"]
if existing.get("pagination", {}).get("total", 0) > 0:
    print("already has transactions, skip seed")
else:
    notes_expense = {
        "Food": ["Canteen lunch", "Coffee with friends", "Pizza night", "Groceries", "Breakfast stall", "Biryani party"],
        "Transport": ["Bus fare", "Uber ride", "Metro ticket", "Rickshaw"],
        "Hostel/Rent": ["Monthly hostel rent"],
        "Academics": ["Print notes", "Lab fees", "Textbook purchase", "Course registration"],
        "Subscriptions": ["Netflix", "Spotify student", "Internet pack"],
        "Entertainment": ["Movie ticket", "Concert", "Gaming credit"],
        "Miscellaneous": ["Stationery", "Laundry", "Mobile recharge"],
    }
    now = datetime.now()
    rows = []
    # income: allowance every month for 4 months
    for m in range(4):
        d = now.replace(day=5) - timedelta(days=30 * m)
        rows.append({"type": "income", "amount": 15000, "categoryId": income_cats[0]["_id"],
                     "note": "Monthly allowance", "date": d.isoformat()})
        if m % 2 == 0:
            rows.append({"type": "income", "amount": 4000, "categoryId": income_cats[1]["_id"],
                         "note": "Part-time tutoring", "date": (d + timedelta(days=10)).isoformat()})
    # expenses over last 120 days
    random.seed(42)
    for i in range(90):
        d = now - timedelta(days=random.randint(0, 119))
        cat = random.choice(expense_cats)
        cname = cat["name"]
        pool = notes_expense.get(cname, ["Expense"])
        amount = {"Food": random.uniform(80, 450), "Transport": random.uniform(40, 250),
                  "Hostel/Rent": random.uniform(3000, 4500), "Academics": random.uniform(100, 1200),
                  "Subscriptions": random.uniform(150, 800), "Entertainment": random.uniform(150, 900),
                  "Miscellaneous": random.uniform(50, 500)}.get(cname, random.uniform(50, 500))
        rows.append({"type": "expense", "amount": round(amount, 2), "categoryId": cat["_id"],
                     "note": random.choice(pool), "date": d.isoformat()})

    for r in rows:
        req("POST", "/transactions", r, token=tok)
    print(f"seeded {len(rows)} transactions")

# budgets
month = now.strftime("%Y-%m")
budgets = req("GET", f"/budgets?month={month}", token=tok)["data"].get("budgets", [])
if not budgets:
    targets = [(c, lim) for c, lim in [
        (next((c for c in expense_cats if c["name"] == "Food"), None), 4000),
        (next((c for c in expense_cats if c["name"] == "Transport"), None), 1500),
        (next((c for c in expense_cats if c["name"] == "Entertainment"), None), 2000),
        (next((c for c in expense_cats if c["name"] == "Academics"), None), 3000),
        (next((c for c in expense_cats if c["name"] == "Subscriptions"), None), 1000),
    ] if c]
    for c, lim in targets:
        req("POST", "/budgets", {"categoryId": c["_id"], "month": month, "limit": lim}, token=tok)
    print(f"seeded {len(targets)} budgets")

# refresh tips
try:
    r = req("POST", "/tips/refresh", {}, token=tok)
    print("tips:", r.get("data", {}).get("generated"))
except Exception as e:
    print("tips err", e)

print("SEED DONE")
