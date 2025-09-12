
#!/usr/bin/env python
# Local SMTP Debug Server using aiosmtpd (prints emails to console)
import argparse, asyncio, logging
from aiosmtpd.controller import Controller

class DebugHandler:
    async def handle_DATA(self, server, session, envelope):
        print("""\n=== SMTP DEBUG SERVER RECEIVED MESSAGE ===
From: {0}
To: {1}
--------------------------------------------
{2}
============================================\n""".format(envelope.mail_from, envelope.rcpt_tos, envelope.content.decode('utf-8', errors='replace')))
        return '250 Message accepted for delivery'

def main():
    p = argparse.ArgumentParser(description="Run a local SMTP debug server")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8025)
    args = p.parse_args()

    controller = Controller(DebugHandler(), hostname=args.host, port=args.port)
    controller.start()
    print(f"SMTP debug server running on {args.host}:{args.port}. Press Ctrl+C to stop.")
    try:
        while True:
            asyncio.get_event_loop().run_until_complete(asyncio.sleep(3600))
    except KeyboardInterrupt:
        print("Stopping debug server...")
    finally:
        controller.stop()

if __name__ == "__main__":
    main()
