import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
from core.utils import extract_emails
import sys
sys.stdout.reconfigure(encoding='utf-8')


COMMON_PATHS = ["", "contact", "about", "team"]

def enrich_url(base_url):
    enriched = {"url": base_url, "emails": "N/A"}

    emails = set()
    for path in COMMON_PATHS:
        try:
            full_url = urljoin(base_url, path)
            print(f"[*] Scraping: {full_url}")
            res = requests.get(full_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code == 200:
                found_emails = extract_emails(res.text)
                emails.update(found_emails)
            time.sleep(1)
        except Exception as e:
            print(f"[!] Error scraping {full_url}: {e}")
            continue

    enriched["emails"] = ", ".join(emails) if emails else "N/A"
    return enriched

def enrich_all(raw_csv="data/leads_raw.csv", out_csv="data/leads_enriched.csv"):
    df = pd.read_csv(raw_csv)
    enriched_data = []

    for idx, row in df.iterrows():
        url = row.get("url") or row.get("link")
        if not isinstance(url, str) or not url.startswith("http"):
            continue
        enriched = enrich_url(url)
        enriched_data.append(enriched)

    pd.DataFrame(enriched_data).to_csv(out_csv, index=False)
    print(f"\n[✓] Enriched {len(enriched_data)} leads saved to {out_csv}")

if __name__ == "__main__":
    enrich_all()
