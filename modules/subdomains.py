"""
Passive subdomain enumeration using crt.sh and certspotter (no API key required).
This module is intentionally passive and low-aggression.
"""
import requests
import time
from utils.logger import info, warn, error

SOURCES = [
    "https://crt.sh/?q=%25.{domain}&output=json",
    "https://certspotter.com/api/v0/certs?domain={domain}&include_subdomains=true",
    "https://rapiddns.io/subdomain/{domain}?full=1",
]

def _fetch_json(url):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "MobileReconX/0.9"})
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        warn(f"source error: {e}")
    return None

def run(domain, concurrency=10, delay=0.1, verbose=False):
    info(f"[subdomains] Enumerating subdomains for: {domain}")
    found = set()

    # crt.sh (works well for many certs)
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        r = requests.get(url, timeout=15, headers={"User-Agent": "MobileReconX/0.9"})
        if r.status_code == 200:
            data = r.json()
            for item in data:
                nv = item.get("name_value") or ""
                for line in nv.splitlines():
                    line = line.strip()
                    if line:
                        found.add(line.replace("*.", ""))
    except Exception:
        pass

    # certspotter (may return list)
    try:
        url = f"https://certspotter.com/api/v0/certs?domain={domain}&include_subdomains=true"
        r = requests.get(url, timeout=12, headers={"User-Agent": "MobileReconX/0.9"})
        if r.status_code == 200:
            data = r.json()
            for cert in data:
                names = cert.get("dns_names", [])
                for n in names:
                    found.add(n.replace("*.", ""))
    except Exception:
        pass

    # add domain itself
    found.add(domain)

    for s in sorted(found):
        print("  →", s)

    info(f"[subdomains] Found {len(found)} unique names")
    # save report
    try:
        import json, os
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/{domain}_subdomains.json", "w") as fh:
            json.dump(sorted(list(found)), fh, indent=2)
        info(f"[subdomains] Saved reports/{domain}_subdomains.json")
    except Exception as e:
        warn(f"Could not save subdomain report: {e}")

    time.sleep(delay)
    return sorted(list(found))
