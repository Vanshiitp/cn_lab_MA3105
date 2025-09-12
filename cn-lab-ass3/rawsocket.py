import socket

HOST, PORT = "127.0.0.1", 9090

def handle_request(data):
    headers = data.split("\r\n")
    cookie = None
    for h in headers:
        if h.startswith("Cookie:"):
            cookie = h.split(":", 1)[1].strip()

    if cookie:
        body = f"<h1>Welcome back! Your cookie: {cookie}</h1>"
        response = ("HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n\r\n" +
                    body)
    else:
        body = "<h1>Hello, new user! Setting your cookie...</h1>"
        response = ("HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "Set-Cookie: User=User123\r\n\r\n" +
                    body)
    return response

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Listening on {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024).decode()
            if not data:
                continue
            response = handle_request(data)
            conn.sendall(response.encode())
