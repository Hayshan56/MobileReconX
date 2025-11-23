#!/usr/bin/env python3

import argparse
import sys
from modules import subdomains, http_probe, fingerprint, dirbrute, cve_lookup

def banner():
    print("""
███▄ ▄███▓ ▒█████  ███▄    █  █    ██  ▄████▄   ▒█████   ██ ▄█▀
▓██▒▀█▀ ██▒▒██▒  ██▒██ ▀█   █  ██  ▓██▒▒██▀ ▀█  ▒██▒  ██▒ ██▄█▒ 
▓██    ▓██░▒██░  ██▓██  ▀█ ██▒▓██  ▒██░▒▓█    ▄ ▒██░  ██▒▓███▄░ 
▒██    ▒██ ▒██   ██▓██▒  ▐▌██▒▓▓█  ░██░▒▓▓▄ ▄██▒▒██   ██░▓██ █▄ 
▒██▒   ░██▒░ ████▓▒▒██░   ▓██░▒▒█████▓ ▒ ▓███▀ ░░ ████▓▒░▒██▒ █▄
░ ▒░   ░  ░░ ▒░▒░▒░░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░░ ▒░▒░▒░ ▒ ▒▒ ▓▒
░  ░      ░  ░ ▒ ▒░░ ░░   ░ ▒░░░▒░ ░ ░   ░  ▒     ░ ▒ ▒░ ░ ░▒ ▒░
░      ░   ░ ░ ░ ▒    ░   ░ ░  ░░░ ░ ░ ░          ░ ░ ░ ▒  ░ ░░ ░ 
       ░       ░ ░          ░    ░     ░ ░            ░ ░  ░  ░   
    Advanced Recon Tool for Termux
""")

def main():
    parser = argparse.ArgumentParser(description="MobileReconX - Advanced Termux Recon Tool")
    parser.add_argument("-d", "--domain", help="Target domain")
    parser.add_argument("--full", action="store_true", help="Run full scan")
    parser.add_argument("--report", action="store_true", help="Generate report")

    args = parser.parse_args()

    banner()

    if not args.domain:
        print("[-] No domain provided")
        sys.exit()

    if args.full:
        subdomains.run(args.domain)
        http_probe.run(args.domain)
        fingerprint.run(args.domain)
        dirbrute.run(args.domain)
        cve_lookup.run(args.domain)

    else:
        print("[*] Use --full to run complete recon.")

if __name__ == "__main__":
    main()
