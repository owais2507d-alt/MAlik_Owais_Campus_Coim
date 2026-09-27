import os
from playwright.sync_api import sync_playwright

OUT = r"D:\campus-coin-master\ppt\screenshots"
os.makedirs(OUT, exist_ok=True)

BASE = "http://localhost:3000"
API = "http://localhost:5000/api/v1"

def shot(page, name, wait=2500):
    page.wait_for_timeout(wait)
    page.screenshot(path=os.path.join(OUT, f"{name}.png"))
    print(f"OK {name}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()

    # Public pages
    page.goto(BASE, wait_until="networkidle", timeout=60000)
    shot(page, "01-landing", 3000)

    page.goto(f"{BASE}/login", wait_until="networkidle", timeout=60000)
    shot(page, "02-login", 2000)

    page.goto(f"{BASE}/register", wait_until="networkidle", timeout=60000)
    shot(page, "03-register", 2000)

    # Login as admin via API on the page context (sets cookies in browser)
    page.goto(f"{BASE}/login", wait_until="networkidle", timeout=60000)
    page.fill('input[name="email"]', "admin@campuscoin.app")
    page.fill('input[name="password"]', "Admin@123")
    page.click('button[type="submit"]')
    page.wait_for_timeout(4000)
    print("URL after login:", page.url)
    shot(page, "04-admin", 4000)

    page.goto(f"{BASE}/admin/users", wait_until="networkidle", timeout=60000)
    shot(page, "05-admin-users", 3000)

    # Logout admin: clear cookies
    ctx.clear_cookies()

    # Login as student
    page.goto(f"{BASE}/login", wait_until="networkidle", timeout=60000)
    page.fill('input[name="email"]', "demo@campuscoin.app")
    page.fill('input[name="password"]', "Demo@123")
    page.click('button[type="submit"]')
    page.wait_for_timeout(4000)
    print("URL after student login:", page.url)
    shot(page, "06-dashboard", 5000)

    page.goto(f"{BASE}/transactions", wait_until="networkidle", timeout=60000)
    shot(page, "07-transactions", 3000)

    page.goto(f"{BASE}/transactions/new", wait_until="networkidle", timeout=60000)
    shot(page, "08-new-transaction", 3000)

    page.goto(f"{BASE}/budgets", wait_until="networkidle", timeout=60000)
    shot(page, "09-budgets", 3000)

    page.goto(f"{BASE}/reports", wait_until="networkidle", timeout=60000)
    shot(page, "10-reports", 4000)

    page.goto(f"{BASE}/tips", wait_until="networkidle", timeout=60000)
    shot(page, "11-tips", 3000)

    page.goto(f"{BASE}/insights", wait_until="networkidle", timeout=60000)
    shot(page, "12-insights", 4000)

    page.goto(f"{BASE}/categories", wait_until="networkidle", timeout=60000)
    shot(page, "13-categories", 3000)

    page.goto(f"{BASE}/transactions/import", wait_until="networkidle", timeout=60000)
    shot(page, "14-csv-import", 3000)

    browser.close()

print("DONE")
