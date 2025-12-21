import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
import re
import json
import sys

HEADERS = {"User-Agent": "DT-Business-Analyst-Scraper"}
IMPORTANT_KEYWORDS = ["about", "company", "product", "products", "solution", "solutions", "industry", "industries", "pricing", "contact", "career", "careers"]
MAX_PAGES = 12

def empty_company_profile():
    return {
        "identity": {"company_name": None, "website": None, "tagline": None},
        "business_summary": {"what_they_do": None, "primary_offerings": [], "target_industries": []},
        "evidence": {"pages_detected": [], "signals": [], "social_links": {}},
        "contact": {"emails": [], "phones": [], "address": None, "contact_page": None},
        "team_hiring": {"careers_page": None, "roles": []},
        "metadata": {"timestamp": None, "pages_crawled": [], "errors": []}
    }

def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.text, None
    except Exception as e:
        return None, str(e)

def extract_emails(text):
    return list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)))

def extract_phones(text):
    return list(set(re.findall(r"\+?\d[\d\s\-()]{7,}", text)))

def extract_social_links(soup):
    socials = {}
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "linkedin.com" in href:
            socials["linkedin"] = href
        elif "twitter.com" in href or "x.com" in href:
            socials["twitter"] = href
        elif "youtube.com" in href:
            socials["youtube"] = href
        elif "instagram.com" in href:
            socials["instagram"] = href
    return socials

def detect_internal_pages(base_url, soup):
    pages = {}
    for link in soup.find_all("a", href=True):
        href = link["href"].lower()
        for key in IMPORTANT_KEYWORDS:
            if key in href and key not in pages:
                pages[key] = urljoin(base_url, link["href"])
    return pages

def extract_homepage(url, profile):
    html, error = fetch_page(url)
    if error:
        profile["metadata"]["errors"].append(f"Homepage error: {error}")
        return None
    soup = BeautifulSoup(html, "html.parser")
    profile["identity"]["website"] = url
    profile["metadata"]["pages_crawled"].append(url)
    if soup.title:
        profile["identity"]["company_name"] = soup.title.get_text(strip=True)
    h1 = soup.find("h1")
    if h1:
        profile["identity"]["tagline"] = h1.get_text(strip=True)
    text = soup.get_text(" ", strip=True)
    profile["contact"]["emails"] = extract_emails(text)
    profile["contact"]["phones"] = extract_phones(text)
    profile["evidence"]["social_links"] = extract_social_links(soup)
    pages = detect_internal_pages(url, soup)
    profile["evidence"]["pages_detected"] = list(pages.values())
    return pages

def crawl_pages(pages, profile):
    count = 0
    for key, page_url in pages.items():
        if count >= MAX_PAGES:
            break
        html, error = fetch_page(page_url)
        if error:
            profile["metadata"]["errors"].append(f"{page_url} error: {error}")
            continue
        soup = BeautifulSoup(html, "html.parser")
        profile["metadata"]["pages_crawled"].append(page_url)
        text = soup.get_text(" ", strip=True)
        if key in ["about", "company"] and not profile["business_summary"]["what_they_do"]:
            paragraphs = soup.find_all("p")
            if paragraphs:
                profile["business_summary"]["what_they_do"] = paragraphs[0].get_text(strip=True)
        if key in ["product", "products", "solution", "solutions"]:
            headings = soup.find_all(["h2", "h3"])
            for h in headings:
                profile["business_summary"]["primary_offerings"].append(h.get_text(strip=True))
        if "contact" in key:
            profile["contact"]["contact_page"] = page_url
            profile["contact"]["emails"].extend(extract_emails(text))
            profile["contact"]["phones"].extend(extract_phones(text))
        if "career" in key:
            profile["team_hiring"]["careers_page"] = page_url
        count += 1

def run(url):
    profile = empty_company_profile()
    pages = extract_homepage(url, profile)
    if pages:
        crawl_pages(pages, profile)
    profile["metadata"]["timestamp"] = datetime.now(timezone.utc).isoformat()
    profile["business_summary"]["primary_offerings"] = list(set(profile["business_summary"]["primary_offerings"]))
    profile["contact"]["emails"] = list(set(profile["contact"]["emails"]))
    profile["contact"]["phones"] = list(set(profile["contact"]["phones"]))
    return profile

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <website_url>")
        sys.exit(1)
    website_url = sys.argv[1]
    result = run(website_url)
    print(json.dumps(result, indent=2))
