"""
CVE lookup using public cve.circl.lu search endpoint.
This is a helper to search for keywords like 'nginx', 'apache', 'openssl' found in server banners.
"""
import requests
from utils.logger import info, warn

BASE = "https://cve.circl.lu/api/search/"

COMMON_PRODUCTS = ["nginx", "apache", "openssl", "jetty", "tomcat", "iis", "php", "wordpress"]

def search_keyword(keyword):
    try:
        r = requests.get(BASE + keyword, timeout=12, headers={"User-Agent":"MobileReconX/0.9"})
        if r.status_code == 200:
            data = r.json()
            return data.get("results") or data
    except Exception as e:
        warn(f"[cve_lookup] error: {e}")
    return []

def run(domain, verbose=False):
    info(f"[cve_lookup] Attempting CVE suggestions for: {domain}")
    # attempt to read previous fingerprint report
    try:
        import json
        with open(f"reports/{domain}_fingerprint.json", "r") as fh:
            fp = json.load(fh)
    except Exception:
        fp = []

    keywords = set()
    for entry in fp:
        server = (entry.get("server") or "").lower()
        cms = (entry.get("cms") or "").lower()
        for p in COMMON_PRODUCTS:
            if p in server or p in cms:
                keywords.add(p)
        # extra heuristics: title or headers
        if entry.get("title"):
            for p in COMMON_PRODUCTS:
                if p in entry.get("title").lower():
                    keywords.add(p)

    # fallback: try common products
    if not keywords:
        keywords.update(COMMON_PRODUCTS[:4])

    all_results = {}
    for k in keywords:
        info(f"[cve_lookup] Searching CVEs for keyword: {k}")
        hits = search_keyword(k)
        all_results[k] = hits[:10]  # keep top 10
        if verbose:
            info(f"[cve_lookup] {k} -> {len(hits)} hits (showing {min(10,len(hits))})")

    try:
        import os, json
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/{domain}_cvelookup.json", "w") as fh:
            json.dump(all_results, fh, indent=2)
        info(f"[cve_lookup] Saved reports/{domain}_cvelookup.json")
    except Exception as e:
        warn(f"[cve_lookup] Could not save report: {e}")

    return all_results
