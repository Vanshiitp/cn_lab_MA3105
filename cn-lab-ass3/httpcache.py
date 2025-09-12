import http.server
import socketserver
import hashlib
import os
import time
from email.utils import formatdate

PORT = 8080
FILE = "index.html"

class CachingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Read file content
            with open(FILE, "rb") as f:
                content = f.read()
            # Generate ETag (MD5 hash of file content)
            etag = hashlib.md5(content).hexdigest()
            # Get Last-Modified time
            last_modified = formatdate(os.path.getmtime(FILE), usegmt=True)
            # Check request headers for caching
            if (self.headers.get("If-None-Match") == etag or
                self.headers.get("If-Modified-Since") == last_modified):
                self.send_response(304)
                self.end_headers()
                return
            # Otherwise, send file with headers
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("ETag", etag)
            self.send_header("Last-Modified", last_modified)
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File Not Found")

with socketserver.TCPServer(("", PORT), CachingHandler) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
