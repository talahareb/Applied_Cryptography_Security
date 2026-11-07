"""Start: python -m demos.tls_server (after generate_certificate)."""
import ssl
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = b'Local HTTPS demonstration: TLS connection established.\n'
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    directory = Path('.local')
    cert, key = directory/'localhost-cert.pem', directory/'localhost-private.key'
    if not cert.exists() or not key.exists():
        raise SystemExit('First run: python -m demos.generate_certificate')
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(str(cert), str(key))
    server = ThreadingHTTPServer(('127.0.0.1', 5443), Handler)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)
    print('Local HTTPS server: https://localhost:5443/ (Ctrl+C to stop)')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
