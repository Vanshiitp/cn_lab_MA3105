
#!/usr/bin/env python
import argparse, sys, socket, datetime, json

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


def query_dnspython(domain: str):
    try:
        import dns.resolver
    except ImportError:
        return None
    results = {"A": [], "MX": [], "CNAME": []}
    resolver = dns.resolver.Resolver()
    # A
    try:
        for r in resolver.resolve(domain, "A"):
            results["A"].append(r.to_text())
    except Exception:
        pass
    # MX
    try:
        for r in resolver.resolve(domain, "MX"):
            results["MX"].append(r.to_text())
    except Exception:
        pass
    # CNAME
    try:
        for r in resolver.resolve(domain, "CNAME"):
            results["CNAME"].append(r.to_text())
    except Exception:
        pass
    return results

def fallback_socket_a(domain: str):
    try:
        ip = socket.gethostbyname(domain)
        return [ip]
    except Exception:
        return []

def main():
    p = argparse.ArgumentParser(description="DNS A/MX/CNAME lookup and log to file")
    p.add_argument("--domain", required=True, help="Domain to query (e.g., example.com)")
    p.add_argument("--out", default="logs/dns_results.txt", help="Path to write DNS results")
    p.add_argument("--log", default="logs/dns.log", help="Log file path")
    args = p.parse_args()

    setup_logging(args.log)
    log = logging.getLogger("dns_client")

    domain = args.domain.strip()
    log.info("DNS query for %s", domain)
    results = query_dnspython(domain)

    if results is None:
        # Fallback for A only
        results = {"A": fallback_socket_a(domain), "MX": [], "CNAME": []}

    # Write results file
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(f"DNS Results for {domain} @ {datetime.datetime.utcnow().isoformat()}Z\n\n")
        for k in ("A", "MX", "CNAME"):
            f.write(f"=== {k} Records ===\n")
            if results.get(k):
                for v in results[k]:
                    f.write(f"- {v}\n")
            else:
                f.write("- (none)\n")
            f.write("\n")

    print(f"Results written to {args.out}")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
