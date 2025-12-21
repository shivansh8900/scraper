# Task 1 — Company Info Web Scraper

This is a Python-based web scraper that extracts structured company information from a given company website URL. The scraper produces a JSON output containing identity, business summary, contact details, social links, hiring signals, and metadata.

---

## Features

- Extracts company identity:
  - Name
  - Website
  - Tagline / one-liner
- Business summary:
  - What they do
  - Primary offerings (products/services)
  - Target customer segments / industries (if available)
- Evidence / Proof:
  - Key pages detected (About, Products, Solutions, Industries, Pricing, Careers, Contact)
  - Social links (LinkedIn, Twitter/X, YouTube, Instagram)
- Contact & Location:
  - Emails
  - Phones
  - Address
  - Contact page URL
- Team & Hiring signals:
  - Careers page URL
  - Roles / departments (if mentioned)
- Metadata:
  - Timestamp of scrape
  - Pages crawled
  - Errors or fallbacks

---

## Dependencies

- Python 3.13+
- Requests
- BeautifulSoup4

Install dependencies using:

```bash
pip install -r requirements.txt

# **How to Run**
python scraper.py <website_url>


Examples:

python scraper.py https://notion.so
python scraper.py https://freshworks.com


Redirect output to JSON file:

python scraper.py https://notion.so > notion.json
python scraper.py https://freshworks.com > freshworks.json


Demo Runs
1. Notion

Command:

python scraper.py https://notion.so


Partial JSON Output:

{
  "identity": {
    "company_name": "The AI workspace that works for you. | Notion",
    "website": "https://notion.so",
    "tagline": "One workspace. Zero busywork."
  },
  "business_summary": {
    "what_they_do": "View all 5,096 employees",
    "primary_offerings": ["API", "Marketing", "Docs", "Startups", "Templates", "Notion AI", "Learn", "Education"]
  },
  "evidence": {
    "pages_detected": ["https://notion.so/product", "https://notion.so/pricing", "https://notion.so/careers"],
    "social_links": {
      "linkedin": "https://www.linkedin.com/company/notionhq/",
      "twitter": "https://twitter.com/NotionHQ"
    }
  },
  "contact": {
    "emails": [],
    "phones": ["300-1999", "100-299"],
    "contact_page": "https://notion.so/contact-sales"
  },
  "team_hiring": {
    "careers_page": "https://notion.so/careers"
  },
  "metadata": {
    "timestamp": "2025-12-20T10:20:15.341191+00:00",
    "pages_crawled": ["https://notion.so", "https://notion.so/product"]
  }
}

2. Freshworks

Command:

python scraper.py https://freshworks.com


Partial JSON Output:

{
  "identity": {
    "company_name": "Freshworks: Uncomplicated Software | IT Service, Customer Service",
    "website": "https://freshworks.com",
    "tagline": "Uncomplicate your IT and customer service"
  },
  "business_summary": {
    "what_they_do": "That belief sparked Freshworks. And it powers everything we do and build today.",
    "primary_offerings": ["Freshsales Suite", "Freshdesk", "Freshservice", "Freshchat"]
  },
  "evidence": {
    "pages_detected": ["https://www.freshworks.com/products/", "https://www.freshworks.com/contact/"],
    "social_links": {
      "linkedin": "https://linkedin.com/company/freshworks-inc",
      "twitter": "https://twitter.com/FreshworksInc"
    }
  },
  "contact": {
    "emails": ["sales@freshworks.com"],
    "phones": ["+91 44 6667 8040", "+1 855 747 6767"],
    "contact_page": "https://www.freshworks.com/contact/"
  },
  "team_hiring": {
    "careers_page": "https://www.freshworks.com/company/careers/"
  },
  "metadata": {
    "timestamp": "2025-12-20T10:25:10.123456+00:00",
    "pages_crawled": ["https://freshworks.com", "https://www.freshworks.com/products/"]
  }
}