"""
MobileReconX - Advanced Recon Tool for Termux
Main entrypoint
"""

import argparse
import sys
import os
from modules import subdomains, http_probe, fingerprint, dirbrute, cve_lookup
from utils.logger import info, warn, error

VERSION = "0.9.0"

def banner():
    print(r"""
███▄ ▄███▓ ▒█████  ███▄    █  █    ██  ▄████▄   ▒█████   ██ ▄█▀
▓██▒▀█▀ ██▒▒██▒  ██▒██ ▀█   █  ██  ▓██▒▒██▀ ▀█  ▒██▒  ██▒ ██▄█▒ 
▓██    ▓██░▒██░  ██▓██  ▀█ ██▒▓██  ▒██░▒▓█    ▄ ▒██░  ██▒▓███▄░ 
▒██    ▒██ ▒██   ██▓██▒  ▐▌██▒▓▓█  ░██░▒▓▓▄ ▄██▒▒██   ██░▓██ █▄ 
▒██▒   ░██▒░ ████▓▒▒██░   ▓██░▒▒█████▓ ▒ ▓███▀ ░░ ████▓▒░▒██▒ █▄
░ ▒░   ░  ░░ ▒░▒░▒░░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░░ ▒░▒░▒░ ▒ ▒▒ ▓▒
░  ░      ░  ░ ▒ ▒░░ ░░   ░ ▒░░░▒░ ░ ░   ░  ▒     ░ ▒ ▒░ ░ ░▒ ▒░
░      ░   ░ ░ ░ ▒    ░   ░ ░  ░░░ ░ ░ ░          ░ ░ ░ ▒  ░ ░░ ░ 
       ░       ░ ░          ░    ░     ░ ░            ░ ░  ░  ░   
    MobileReconX — Advanced Recon Tool for Termux (ethical use only)
    Version: {}
""".format(VERSION))

def main():
    parser = argparse.ArgumentParser(prog="mobilereconx",
                                     description="MobileReconX - Advanced Termux Recon Tool (ethical use only)")
    parser.add_argument("-d", "--domain", help="Target domain (example.com)", required=True)
    parser.add_argument("--full", action="store_true", help="Run full recon (subdomains, probe, fingerprint, dirbrute, cve)")
    parser.add_argument("--sub", action="store_true", help="Run subdomain enumeration only")
    parser.add_argument("--probe", action="store_true", help="Run HTTP probing only")
    parser.add_argument("--finger", action="store_true", help="Run fingerprinting only")
    parser.add_argument("--dir", action="store_true", help="Run directory brute force only")
    parser.add_argument("--cve", action="store_true", help="Do CVE lookup for discovered services")
    parser.add_argument("--report", action="store_true", help="Save JSON/HTML report to reports/")
    parser.add_argument("--safe", action="store_true", help="Enable safe mode (low concurrency, polite delays)")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrency for async tasks (default 10)")
    parser.add_argument("--delay", type=float, default=0.15, help="Delay between requests in seconds (default 0.15)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    banner()

    # basic checks
    if not args.domain:
        error("No domain provided. Use -d example.com")
        sys.exit(1)

    # create reports dir
    os.makedirs("reports", exist_ok=True)

    info(f"Target: {args.domain}")
    if args.safe:
        info("Safe mode ON: reduced concurrency and polite delay")
        args.concurrency = min(args.concurrency, 8)
        args.delay = max(args.delay, 0.2)

    try:
        if args.full or args.sub:
            subdomains.run(args.domain, concurrency=args.concurrency, delay=args.delay, verbose=args.verbose)

        if args.full or args.probe:
            http_probe.run(args.domain, concurrency=args.concurrency, delay=args.delay, verbose=args.verbose)

        if args.full or args.finger:
            fingerprint.run(args.domain, concurrency=args.concurrency, delay=args.delay, verbose=args.verbose)

        if args.full or args.dir:
            dirbrute.run(args.domain, wordlist="modules/wordlists/common_dirs.txt",
                        concurrency=args.concurrency, delay=args.delay, verbose=args.verbose)

        if args.full or args.cve:
            cve_lookup.run(args.domain, verbose=args.verbose)

        if args.report:
            info("Report generation is implemented per-module; check reports/ for JSON/HTML outputs.")

        info("Run complete. Check reports/ and logs/ for details.")
    except KeyboardInterrupt:
        warn("Interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
