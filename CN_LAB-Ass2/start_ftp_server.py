
#!/usr/bin/env python
# Local FTP server using pyftpdlib
import argparse, os
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

def main():
    p = argparse.ArgumentParser(description="Run a local FTP server for testing")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=2121)
    p.add_argument("--user", default="user")
    p.add_argument("--password", default="12345")
    p.add_argument("--home", default="./ftp_home")
    args = p.parse_args()

    os.makedirs(args.home, exist_ok=True)

    authorizer = DummyAuthorizer()
    # Permissions: "elradfmwMT" = all
    authorizer.add_user(args.user, args.password, args.home, perm="elradfmwMT")
    authorizer.add_anonymous(args.home, perm="elr")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer((args.host, args.port), handler)
    print(f"FTP server running on {args.host}:{args.port} (user={args.user} / password={args.password})")
    print(f"Home directory: {os.path.abspath(args.home)}")
    server.serve_forever()

if __name__ == "__main__":
    main()
