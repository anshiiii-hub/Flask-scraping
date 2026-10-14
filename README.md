# Flask-scraping

A Flask portfolio site for my web-scraping and data-analysis projects. Each project gets its own page, with the report and dataset available to view or download.

## What's on the site

- **Web-scraping projects:** Books to Scrape, Amazon facewash products, Flipkart laptops, Goodreads quotes, top mutual funds, crypto gainers.
- **Data-science projects:** stock market analysis, IPL analysis, UPI analysis.
- **Other pages:** home, projects, about me, blogs, journey, AI/ML, Power BI, and a GitHub page that pulls my public repositories from the GitHub API.
- **Downloads:** every project page can serve its CSV from `data/` and its PDF report from `pdf/`, either as a download or opened in the browser.

The datasets were collected beforehand and saved as CSV files, so the site reads those files rather than scraping live.

## Tech

Python · Flask · pandas · requests · Jinja templates · HTML, CSS and JavaScript

## Project structure

```
app.py                         Flask routes and page logic
templates/                     HTML pages (Jinja)
static/                        CSS, JavaScript, images
data/                          CSV datasets
pdf/                           PDF reports
FILE_CONNECTIONS_SUMMARY.md    notes on how pages map to files
WEB_SCRAPING_FIXES_SUMMARY.md  notes on scraping fixes
```

## Run it locally

```bash
git clone https://github.com/anshiiii-hub/Flask-scraping.git
cd Flask-scraping
pip install -r requirements.txt
python app.py
```

Then open http://localhost:3000.

## Notes

- The GitHub page needs an internet connection to call the GitHub API.
- Live stock prices are switched off in the code, so the stock market page uses sample data.
