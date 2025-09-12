
# Computer Networks Lab — Assignment 2 (HTTP, SMTP, FTP, DNS)

This repo contains **fully working reference implementations** for each protocol:
- `http_client.py` — HTTP GET/POST using `requests` with logging and error handling.
- `smtp_client.py` — SMTP client using Python's `smtplib`. Works with any SMTP server (e.g., Gmail SMTP or a local debug SMTP server).
- `ftp_client.py` — FTP client using `ftplib` (upload, download, list) + optional **local FTP test server**.
- `dns_client.py` — DNS lookups for A, MX, and CNAME records; logs results to a file.

It also includes optional **local test servers** so you can run everything offline/on LAN:
- `start_smtp_debug_server.py` — Runs a local SMTP debug server on `localhost:8025` via `aiosmtpd` (emails are printed to console).
- `start_ftp_server.py` — Runs a local FTP server on `localhost:2121` via `pyftpdlib` with a test user.

## 1) Environment Setup

```bash
python -V           # Python 3.10+ recommended
python -m venv .venv
.venv\Scripts\activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> If your Python is 3.12+, `smtpd` (stdlib) is deprecated. We use **aiosmtpd** for a local SMTP debug server.

## 2) How to Run Each Part

### A) HTTP
Run:
```bash
python http_client.py --url https://httpbin.org/get --post-url https://httpbin.org/post
```
Outputs:
- Prints status, headers, and body.
- Logs to `logs/http.log`.

### B) SMTP
**Option 1 — Use local debug SMTP (no email actually sent):**
1. Open a new terminal and run:
    ```bash
    python start_smtp_debug_server.py --host 127.0.0.1 --port 8025
    ```
2. In another terminal, send a test email:
    ```bash
    python smtp_client.py --host 127.0.0.1 --port 8025 --from you@example.com --to test@local --subject "Hello from CN2" --body "This is a local SMTP test"
    ```
   The server terminal will print the email contents.

**Option 2 — Use a real SMTP server (example: Gmail):**
```bash
python smtp_client.py --host smtp.gmail.com --port 587 --starttls   --username YOUR_EMAIL --password YOUR_APP_PASSWORD   --from YOUR_EMAIL --to RECIPIENT_EMAIL   --subject "CN2 Test" --body "Hello via Gmail SMTP"
```
> For Gmail, set up an **App Password** with 2FA; plain password login will fail.

Logs:
- Client logs to `logs/smtp.log`.

### C) FTP
**Start a local FTP server (recommended for demo):**
```bash
python start_ftp_server.py --host 127.0.0.1 --port 2121 --user user --password 12345 --home ./ftp_home
```
- It creates `ftp_home` folder and an account `user / 12345`.
- Leave this running in one terminal.

**Run the FTP client from another terminal:**
```bash
# Upload a file, list dirs, download it back to downloads/, verify content
python ftp_client.py --host 127.0.0.1 --port 2121 --user user --password 12345   --upload sample_upload.txt --remote-name uploaded_sample.txt   --download uploaded_sample.txt --download-dir downloads
```
Outputs:
- Prints actions and verification.
- Logs to `logs/ftp.log`.

> You can also point `--host` to any real FTP server you have credentials for.

### D) DNS
Run:
```bash
python dns_client.py --domain example.com --out logs/dns_results.txt
```
- Prints A, MX, CNAME results and writes them to `logs/dns_results.txt`.
- Logs to `logs/dns.log`.

## 3) Run Everything (Demo Orchestrator)
This runs simple happy-path demos. For SMTP/FTP, **start the local servers first** as shown above, then:
```bash
python run_all.py
```

## 4) Files to Put Where
Place all files in a single folder (this repo root). Important paths created at runtime:
- `logs/` — protocol logs + DNS output.
- `downloads/` — FTP downloads.
- `ftp_home/` — created by the local FTP server (if used).

## 5) Notes
- All scripts use robust logging and error handling.
- Network calls depend on connectivity and server availability; using local servers ensures testability.
- For submission, include screenshots of terminal outputs and the generated log files in `logs/`.

