# main.py

import asyncio
import pandas as pd
import sys

# Attempt to import Playwright
try:
    from playwright.async_api import async_playwright
except ModuleNotFoundError:
    print("\n[ERROR] The 'playwright' module is not installed. Please run:\n")
    print("    pip install playwright")
    print("    playwright install\n")
    sys.exit(1)

# Constants
BASE_URL = "https://www.ycombinator.com/companies"
CONCURRENCY = 5  # Number of pages to scrape concurrently

# Data storage
data = []

# -----------------------------------------------------------------------------
# Function: scrape_founder_info
# Purpose: Visit individual company page and extract founder names and LinkedIn URLs
# -----------------------------------------------------------------------------
async def scrape_founder_info(browser, company, index):
    try:
        page = await browser.new_page()
        await page.goto(company["Company url"], timeout=60000, wait_until="domcontentloaded")
        await page.wait_for_timeout(1500)

        founder_blocks = await page.query_selector_all("div[class*='min-w-0']")
        founder_names = []
        linkedin_urls = []

        # Extract founder name and LinkedIn if available
        for block in founder_blocks:
            name_el = await block.query_selector("div[class*='font-bold']")
            name = await name_el.inner_text() if name_el else ""
            if name:
                founder_names.append(name)

            linkedin_el = await block.query_selector("a[href*='linkedin.com/in']")
            linkedin = await linkedin_el.get_attribute("href") if linkedin_el else ""
            if linkedin:
                linkedin_urls.append(linkedin)

        # Add to the company record
        company["Founder Name(s)"] = ", ".join(founder_names)
        company["Founder LinkedIn URL(s)"] = ", ".join(linkedin_urls)

        print(f"[{index+1}] ✅ {company['Company Name']} — Founders: {len(founder_names)}")
        await page.close()

    except Exception as e:
        company["Founder Name(s)"] = ""
        company["Founder LinkedIn URL(s)"] = ""
        print(f"[{index+1}] ⚠️ Failed to scrape {company['Company Name']}: {e}")

# -----------------------------------------------------------------------------
# Function: scrape_all_profiles
# Purpose: Run founder scraping in concurrent batches to speed up execution
# -----------------------------------------------------------------------------
async def scrape_all_profiles(browser, companies):
    for i in range(0, len(companies), CONCURRENCY):
        batch = companies[i:i+CONCURRENCY]
        await asyncio.gather(*(scrape_founder_info(browser, c, i + j) for j, c in enumerate(batch)))

# -----------------------------------------------------------------------------
# Function: scrape_yc_companies
# Purpose: Scrapes YC startup listings and their founder details
# -----------------------------------------------------------------------------
async def scrape_yc_companies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL, timeout=60000, wait_until="domcontentloaded")

        # Scroll to trigger lazy-loading of more startups
        print("Scrolling and loading companies...")
        for _ in range(32):
            await page.mouse.wheel(0, 10000)
            await page.wait_for_timeout(1500)

        # Extract company listing elements
        print("Extracting company cards...")
        cards = await page.query_selector_all("a[class*='_company']")
        print(f"Found {len(cards)} companies")

        # Loop through each card to extract summary info
        for i, card in enumerate(cards[:500]):
            name = await card.query_selector("span[class*='_coName']")
            desc = await card.query_selector("span[class*='_coDescription']")
            batch_span = await card.query_selector("a[href*='?batch='] span")

            name_text = await name.inner_text() if name else ""
            desc_text = await desc.inner_text() if desc else ""
            batch_text = await batch_span.inner_text() if batch_span else ""

            href = await card.get_attribute("href")
            company_url = f"https://www.ycombinator.com{href}" if href else ""

            if i < 2:
                print(f"[{i+1}] Scraping: {company_url}")

            data.append({
                "Company Name": name_text,
                "Batch": batch_text,
                "Short Description": desc_text,
                "Company url": company_url
            })

        # Concurrently scrape founder details for each company
        print("Scraping founder details concurrently...")
        await scrape_all_profiles(browser, data)

        # Close browser and save data
        await browser.close()
        df = pd.DataFrame(data)
        df.to_csv("yc_startup.csv", index=False)
        print("✅ Saved to yc_startups.csv")

# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    asyncio.run(scrape_yc_companies())
