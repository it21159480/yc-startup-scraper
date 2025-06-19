# 🚀 YC Startup Scraper

A lightning-fast, Playwright-powered Python scraper that extracts rich data from [Y Combinator’s Startup Directory](https://www.ycombinator.com/companies) — engineered with **async concurrency** for performance and precision.

> This is a personal project built to explore intelligent web scraping, asynchronous Python, and real-world data automation using Playwright.
---

## 📊 What It Extracts

For each startup, the scraper collects:

- 🏢 **Company Name**
- 🚀 **Batch** (e.g., Summer 2022)
- ✍️ **Short Description**
- 👤 **Founder Names**
- 🔗 **LinkedIn Profiles** *(if available)*

---

## ⚙️ Tech Stack

| Tool         | Purpose                            |
|--------------|-------------------------------------|
| 🐍 Python 3.10+ | Core scripting logic               |
| 🎭 Playwright | Browser automation & scraping      |
| 🔄 Asyncio     | Fast, concurrent scraping          |
| 📦 Pandas     | Clean tabular export to CSV        |

---

## 📁 Output

Results are saved in a clean CSV file:

```bash
yc_startup.csv
```
> Each row represents a startup, neatly organized with all the fields listed above.





---

## 🚀 Quick Start

1.  📥**Install dependencies**
```bash
pip install pandas playwright
playwright install
```
2.  🏁**Run the scraper**
```bash
python main.py
```
> Scraping begins, with real-time logs showing progress. The output CSV will be created when done.


---
## 📌 Project Goal

This project was created to demonstrate:

- **Smart scraping of dynamic web pages**
- **Handling JavaScript-heavy content with Playwright**
- **Async Python for concurrent browser automation**
- **Clean, structured data collection from real startup ecosystems**

---
## 🧠 Future Ideas
- ✨ **Add resume/continue support**

- 📥 **Save failed URLs for retry**

- 🌐 **Enrich founder data with external APIs (LinkedIn search, Google Custom Search)**




