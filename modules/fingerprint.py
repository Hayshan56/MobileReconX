"""
Lightweight fingerprinting:
- Detect WAF via header/pattern checks
- Detect CMS by common paths and meta generator tags
- Basic server technology inference
"""
import requests
import re
from bs4 import BeautifulSoup
from utils.logger import info, warn

CMS_SIGS = {
    "wordpress": ["/wp-login.php", "/wp-admin/", "wp-content", "WordPress"],
    "joomla": ["/administrator/", "Joomla"],
    "drupal": ["sites/default", "Drupal"],
    "shopify": ["cdn.shopify.com", "X-Shopify-Stage"],
}

WAF_SIGS = [
    "cloudflare",
    "sucuri",
    "incapsula",
    "akamai",
    "f5",
    "mod_security",
    "deny",
]

def _check_waf(headers, body):
    server = (headers.get("Server") or "").lower()
    combined = " ".join([server, str(headers).lower(), str(body).lower()])
    for sig in WAF_SIGS:
        if sig in combined:
            return sig
    return None

def _detect_cms(base_url):
    try:
        r = requests.get(base_url, timeout=10, headers={"User-Agent":"MobileReconX/0.9"})
        text = r.text or ""
        soup = BeautifulSoup(text, "html.parser")
        # generator meta
        gen = soup.find("meta", attrs={"name":"generator"})
        if gen and gen.get("content"):
            return gen.get("content")
        # path and content checks
        for cms, checks in CMS_SIGS.items():
            for c in checks:
                if c.lower() in text.lower() or c.lower() in r.url.lower():
                    return cms
    except Exception as e:
        warn(f"[fingerprint] CMS check error: {e}")
    return None

def run(domain, concurrency=8, delay=0.12, verbose=False):
    info(f"[fingerprint] Running fingerprinting for: {domain}")
    urls = [f"https://{domain}/", f"http://{domain}/"]
    results = []

    for u in urls:
        try:
            r = requests.get(u, timeout=12, headers={"User-Agent":"MobileReconX/0.9"}, allow_redirects=True)
            waf = _check_waf(r.headers, r.text)
            cms = _detect_cms(u)
            server = r.headers.get("Server")
            item = {
                "url": u,
                "status": r.status_code,
                "server": server,
                "waf": waf,
                "cms": cms,
                "title": BeautifulSoup(r.text, "html.parser").title.string if BeautifulSoup(r.text, "html.parser").title else None
            }
            results.append(item)
            if verbose:
                info(f"[fingerprint] {u} -> status {r.status_code} server={server} waf={waf} cms={cms}")
        except Exception as e:
            warn(f"[fingerprint] {u} -> {e}")

    # save report
    try:
        import json, os
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/{domain}_fingerprint.json", "w") as fh:
            json.dump(results, fh, indent=2)
        info(f"[fingerprint] Saved reports/{domain}_fingerprint.json")
    except Exception as e:
        warn(f"[fingerprint] could not save report: {e}")

    return results
