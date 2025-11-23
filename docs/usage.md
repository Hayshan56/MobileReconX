# MobileReconX - Usage notes

- Use `--safe` on initial runs; it reduces concurrency and adds delays.
- Directory brute force ships with a small wordlist; replace or append your own lists in `modules/wordlists/`.
- CVE lookup is a helper; always verify matches manually.
- Reports are in `reports/` as JSON. You can import them into other tooling for correlation.
