"""
Async directory brute for common admin and backup paths.
This module runs politely by default. Use --safe to avoid high load.
"""
import asyncio
import aiohttp
import time
from urllib.parse import urljoin
from utils.logger import info, warn

# small default wordlist shipped with the tool (terms are common; extend locally)
DEFAULT_WORDLIST = "modules/wordlists/common_dirs.txt"

async def _fetch(session, url):
    try:
        async with session.get(url, allow_redirects=True, timeout=15) as r:
            return (url, r.status)
    except Exception:
        return (url, None)

async def _brute(base, paths, concurrency, delay):
    connector = aiohttp.TCPConnector(limit_per_host=concurrency)
    timeout = aiohttp.ClientTimeout(total=30)
    found = []
    async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers={"User-Agent":"MobileReconX/0.9"}) as session:
        sem = asyncio.Semaphore(concurrency)
        tasks = []

        async def worker(p):
            async with sem:
                url = urljoin(base, p)
                u, status = await _fetch(session, url)
                if status and status < 400:
                    found.append((u, status))
                await asyncio.sleep(delay)

        for p in paths:
            tasks.append(asyncio.create_task(worker(p.strip().lstrip("/"))))
        await asyncio.gather(*tasks)
    return found

def run(domain, wordlist=DEFAULT_WORDLIST, concurrency=10, delay=0.15, verbose=False):
    info(f"[dirbrute] Running directory brute against: {domain}")
    bases = [f"https://{domain}/", f"http://{domain}/"]
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as fh:
        paths = [l.strip() for l in fh if l.strip() and not l.startswith("#")]

    results = []
    for base in bases:
        try:
            found = asyncio.run(_brute(base, paths, concurrency, delay))
            for u, status in found:
                info(f"  [+] {status} -> {u}")
            results.extend(found)
        except Exception as e:
            warn(f"[dirbrute] {base} -> {e}")

    # save report
    try:
        import json, os
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/{domain}_dirbrute.json", "w") as fh:
            json.dump(results, fh, indent=2)
        info(f"[dirbrute] Saved reports/{domain}_dirbrute.json")
    except Exception as e:
        warn(f"[dirbrute] Could not save report: {e}")

    return results
