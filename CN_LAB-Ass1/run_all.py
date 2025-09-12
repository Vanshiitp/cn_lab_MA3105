
#!/usr/bin/env python
# Orchestrates quick demo runs. Requires that you have started local servers for SMTP and FTP first.
import subprocess, sys, os, shutil

def run(cmd):
    print("\n$ " + " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("Command failed:", e)

def main():
    # HTTP
    run([sys.executable, "http_client.py", "--url", "https://httpbin.org/get", "--post-url", "https://httpbin.org/post"])

    # SMTP (assumes local debug SMTP running on 127.0.0.1:8025)
    run([sys.executable, "smtp_client.py", "--host", "127.0.0.1", "--port", "8025",
         "--from", "demo@local", "--to", "receiver@local",
         "--subject", "CN2 Orchestrator Test", "--body", "Hello from run_all.py via local SMTP!"])

    # FTP (assumes local FTP server on 127.0.0.1:2121 with user/password)
    if not os.path.exists("sample_upload.txt"):
        with open("sample_upload.txt", "w", encoding="utf-8") as f:
            f.write("Hello from CN2 FTP upload test.\n")
    run([sys.executable, "ftp_client.py", "--host", "127.0.0.1", "--port", "2121",
         "--user", "user", "--password", "12345",
         "--upload", "sample_upload.txt", "--remote-name", "uploaded_sample.txt",
         "--download", "uploaded_sample.txt", "--download-dir", "downloads"])

    # DNS
    run([sys.executable, "dns_client.py", "--domain", "example.com", "--out", "logs/dns_results.txt"])

if __name__ == "__main__":
    main()
