import requests

def run(domain):
    print(f"\n[+] Enumerating subdomains for: {domain}")

    urls = [
        f"https://crt.sh/?q=%25.{domain}&output=json",
    ]

    found = set()

    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                for item in data:
                    sub = item["name_value"]
                    found.add(sub.replace("*.", ""))
        except:
            pass

    for s in sorted(found):
        print("  →", s)

    print(f"[✓] Found {len(found)} subdomains")
