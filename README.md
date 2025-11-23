# MobileReconX

**MobileReconX** — Advanced Termux recon tool for subdomains, HTTP probing, fingerprinting, directory brute force (polite), and CVE suggestions.
[![file-000000004798720792256ee3adc8362c.png](https://i.postimg.cc/htXXSzL4/file-000000004798720792256ee3adc8362c.png)](https://postimg.cc/YvwrRSDT)
> ⚠️ **Only use MobileReconX on systems you own or have explicit permission to test. Unauthorized scanning is illegal.**

## Features
- Passive subdomain enumeration (crt.sh, certspotter)
- HTTP probing (headers, redirects, server banners)
- Lightweight fingerprinting (WAF, CMS detection)
- Async directory brute force (polite defaults)
- CVE lookup suggestions using public endpoints
- JSON reports saved to `reports/`
- Safe mode to reduce aggression

## Quick start (Termux)
```bash
# 1) clone
git clone git@github.com:Hayshan56/MobileReconX.git
cd MobileReconX

# 2) install
bash install.sh

# 3) run (safe default)
./mobilereconx.py -d example.com --full --report --safe
