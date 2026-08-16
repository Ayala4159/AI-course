from playwright.sync_api import sync_playwright

try:
    print("Starting Playwright...")
    p = sync_playwright().start()
    print("Launching browser...")
    browser = p.chromium.launch()
    print("Creating page...")
    page = browser.new_page()
    print("Going to website...")
    page.goto('https://www.weather2day.co.il/forecast')
    print(f"Page title: {page.title()}")
    print("Test successful!")
    browser.close()
    p.stop()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
