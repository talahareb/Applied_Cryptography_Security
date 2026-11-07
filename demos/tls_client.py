"""Run: python -m demos.tls_client (in second terminal)."""
import ssl
import socket
from pathlib import Path
from cryptography import x509


def main():
    cert_path = Path('.local/localhost-cert.pem')
    if not cert_path.exists():
        raise SystemExit('First generate the local certificate.')
    # Hostname checking and signature verification remain ENABLED.
    ctx = ssl.create_default_context(cafile=str(cert_path))
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    with socket.create_connection(('127.0.0.1', 5443), timeout=5) as sock:
        with ctx.wrap_socket(sock, server_hostname='localhost') as tls:
            # Capture TLS metadata while the connection remains active.
            version = tls.version()
            cipher = tls.cipher()[0]
            cert = x509.load_der_x509_certificate(tls.getpeercert(binary_form=True))
            tls.sendall(b'GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n')
            chunks = []
            while True:
                data = tls.recv(8192)
                if not data: break
                chunks.append(data)
            print('Negotiated TLS:', version)
            print('Cipher:', cipher)
            print('X.509 subject:', cert.subject.rfc4514_string())
            print('Certificate valid until:', cert.not_valid_after_utc.isoformat())
            print('Response:\n' + b''.join(chunks).decode(errors='replace'))


if __name__ == '__main__':
    main()
