
#!/usr/bin/env python
import argparse, smtplib, ssl
from email.message import EmailMessage

import logging, sys, os

def setup_logging(log_path: str):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    p = argparse.ArgumentParser(description="SMTP client (supports STARTTLS)")
    p.add_argument("--host", required=True, help="SMTP host (e.g., 127.0.0.1 or smtp.gmail.com)")
    p.add_argument("--port", type=int, required=True, help="SMTP port (e.g., 8025 for local debug, 587 for Gmail)")
    p.add_argument("--starttls", action="store_true", help="Use STARTTLS")
    p.add_argument("--username", help="SMTP username (optional)")
    p.add_argument("--password", help="SMTP password (optional)")
    p.add_argument("--from", dest="from_addr", required=True, help="From address")
    p.add_argument("--to", dest="to_addr", required=True, help="Recipient address")
    p.add_argument("--subject", default="CN2 Test", help="Email subject")
    p.add_argument("--body", default="Hello from CN2 SMTP client.", help="Email body")
    p.add_argument("--log", default="logs/smtp.log", help="Log file path")
    args = p.parse_args()

    setup_logging(args.log)
    log = logging.getLogger("smtp_client")

    msg = EmailMessage()
    msg["From"] = args.from_addr
    msg["To"] = args.to_addr
    msg["Subject"] = args.subject
    msg.set_content(args.body)

    try:
        if args.starttls:
            context = ssl.create_default_context()
            with smtplib.SMTP(args.host, args.port, timeout=20) as server:
                log.info("Connected to %s:%s", args.host, args.port)
                server.ehlo()
                server.starttls(context=context)
                log.info("STARTTLS negotiated")
                server.ehlo()
                if args.username and args.password:
                    server.login(args.username, args.password)
                    log.info("Logged in as %s", args.username)
                server.send_message(msg)
                log.info("Email sent to %s", args.to_addr)
                print("Email sent successfully.")
        else:
            with smtplib.SMTP(args.host, args.port, timeout=20) as server:
                log.info("Connected to %s:%s", args.host, args.port)
                server.ehlo()
                if args.username and args.password:
                    server.login(args.username, args.password)
                    log.info("Logged in as %s", args.username)
                server.send_message(msg)
                log.info("Email sent to %s", args.to_addr)
                print("Email sent successfully.")
    except Exception as e:
        log.exception("SMTP send failed: %s", e)
        print("SMTP error:", e)

if __name__ == "__main__":
    main()
