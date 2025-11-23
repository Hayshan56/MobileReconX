#!/usr/bin/env bash
set -e

echo "[*] MobileReconX — Installing dependencies for Termux"

# ---- Update system ----
pkg update -y
pkg upgrade -y

# ---- Install required Termux packages ----
pkg install -y python git curl openssh nano bash \
               clang libxml2 libxslt openssl

# ---- Install Python build dependencies ----
# (aiohttp needs this sometimes)
pkg install -y python-pip wheel

echo "[*] Installing Python modules (do NOT upgrade pip)"
pip install --no-cache-dir -r requirements.txt

# ---- Make main script executable ----
chmod +x mobilereconx.py

echo "[*] Installation complete!"
echo "Run example:"
echo "python3 mobilereconx.py -d example.com --full"
