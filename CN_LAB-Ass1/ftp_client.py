
#!/usr/bin/env python
import argparse, os, io, sys
from ftplib import FTP, error_perm

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
    p = argparse.ArgumentParser(description="FTP client: upload, list, download, verify")
    p.add_argument("--host", required=True)
    p.add_argument("--port", type=int, default=21)
    p.add_argument("--user", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--upload", help="Local file to upload (optional)")
    p.add_argument("--remote-name", help="Remote filename for upload (optional)")
    p.add_argument("--download", help="Remote filename to download (optional)")
    p.add_argument("--download-dir", default="downloads", help="Local directory to save downloads")
    p.add_argument("--log", default="logs/ftp.log", help="Log file path")
    args = p.parse_args()

    setup_logging(args.log)
    log = logging.getLogger("ftp_client")

    try:
        with FTP() as ftp:
            ftp.connect(args.host, args.port, timeout=20)
            log.info("Connected to %s:%s", args.host, args.port)
            ftp.login(args.user, args.password)
            log.info("Logged in as %s", args.user)

            # List directory
            print("Directory listing:")
            ftp.retrlines("LIST")

            # Upload
            if args.upload and args.remote_name:
                if not os.path.exists(args.upload):
                    raise FileNotFoundError(f"Local file not found: {args.upload}")
                with open(args.upload, "rb") as f:
                    ftp.storbinary(f"STOR {args.remote_name}", f)
                log.info("Uploaded %s -> %s", args.upload, args.remote_name)
                print(f"Uploaded: {args.upload} -> {args.remote_name}")

            # Download
            if args.download:
                os.makedirs(args.download_dir, exist_ok=True)
                local_path = os.path.join(args.download_dir, os.path.basename(args.download))
                with open(local_path, "wb") as f:
                    ftp.retrbinary(f"RETR {args.download}", f.write)
                log.info("Downloaded %s -> %s", args.download, local_path)
                print(f"Downloaded: {args.download} -> {local_path}")

                # Verify (size compare)
                remote_size = ftp.size(args.download)
                local_size = os.path.getsize(local_path)
                if remote_size == local_size:
                    print("Verification OK: file sizes match.")
                else:
                    print(f"Verification WARNING: remote_size={remote_size}, local_size={local_size}")

    except Exception as e:
        log.exception("FTP error: %s", e)
        print("FTP error:", e)

if __name__ == "__main__":
    main()
