
#!/usr/bin/env python
import argparse
import requests
from requests.exceptions import RequestException

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
    p = argparse.ArgumentParser(description="HTTP GET/POST client")
    p.add_argument("--url", default="https://httpbin.org/get", help="GET URL")
    p.add_argument("--post-url", default="https://httpbin.org/post", help="POST URL")
    p.add_argument("--post-data", default='{"hello": "world"}', help="POST JSON data as string")
    p.add_argument("--log", default="logs/http.log", help="Log file path")
    args = p.parse_args()

    setup_logging(args.log)
    log = logging.getLogger("http_client")

    try:
        log.info("Sending GET to %s", args.url)
        r = requests.get(args.url, timeout=15)
        print("GET status:", r.status_code)
        print("GET headers:", dict(r.headers))
        print("GET body:", r.text[:500], "..." if len(r.text) > 500 else "")
    except RequestException as e:
        log.exception("GET request failed: %s", e)

    try:
        log.info("Sending POST to %s", args.post_url)
        r = requests.post(args.post_url, json={"data": args.post_data}, timeout=15)
        print("POST status:", r.status_code)
        print("POST headers:", dict(r.headers))
        print("POST body:", r.text[:500], "..." if len(r.text) > 500 else "")
    except RequestException as e:
        log.exception("POST request failed: %s", e)

if __name__ == "__main__":
    main()
