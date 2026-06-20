from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://itea.co.il/en/")
        page.wait_for_load_state("domcontentloaded")
        
        # Click the target item using JS to bypass any animation overlaps
        page.locator('a:has-text("relaxation")').first.evaluate("node => node.click()")
        page.wait_for_load_state("domcontentloaded")
        print("URL:", page.url)

        browser.close()

run()
