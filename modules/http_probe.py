"""
HTTP probing module. Uses requests (sync) for reliability on Termux.
Checks HTTP status, headers, server banners, redirect chains, TLS info (basic).
"""
import requests
import time
from urllib.parse import urljoin
from utils.logger import info, warn

DEFAULT_PATHS = ["/", "/robots.txt", "/.well-known/security.txt"]

def _probe_url(url, timeout=15):
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "MobileReconX/0.9"})
        data = {
            "url": url,
            "status_code": r.status_code,
            "final_url": r.url,
            "history": [h.status_code for h in r.history],
            "server": r.headers.get("Server"),
            "content_type": r.headers.get("Content-Type"),
            "headers": dict(r.headers),
            "length": len(r.content),
            "reason": r.reason,
        }
        return data
    except Exception as e:
        warn(f"[http_probe] {url} -> {e}")
        return None

def run(domain, concurrency=10, delay=0.12, verbose=False):
    info(f"[http_probe] Probing http(s) for: {domain}")
    scheme_candidates = ["https://", "http://"]
    results = []

    for scheme in scheme_candidates:
        base = f"{scheme}{domain}"
        for p in DEFAULT_PATHS:
            url = urljoin(base, p)
            r = _probe_url(url)
            if r:
                results.append(r)
                if verbose:
                    info(f"  {r['status_code']} {r['final_url']} ({r['server']})")
            time.sleep(delay)

    # Save basic report
    try:
        import json, os
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/{domain}_http_probe.json", "w") as fh:
            json.dump(results, fh, indent=2)
        info(f"[http_probe] Saved reports/{domain}_http_probe.json")
    except Exception as e:
        warn(f"[http_probe] Could not save report: {e}")

    return results
