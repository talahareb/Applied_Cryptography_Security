"""Generate local-only self-signed X.509 certificates for the TLS demo."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from ipaddress import IPv4Address
import os
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.x509.oid import NameOID


def generate_local_cert(output_dir: Path, algorithm: str = 'ECDSA') -> tuple[Path, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if algorithm.upper() == 'RSA':
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    elif algorithm.upper() == 'ECDSA':
        key = ec.generate_private_key(ec.SECP256R1())
    else:
        raise ValueError('algorithm must be ECDSA or RSA')
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder()
        .subject_name(name).issuer_name(name).public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=5))
        .not_valid_after(now + timedelta(days=7))
        .add_extension(x509.SubjectAlternativeName([
            x509.DNSName('localhost'), x509.IPAddress(IPv4Address('127.0.0.1'))
        ]), critical=False)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(key, hashes.SHA256()))
    cert_path = output_dir/'localhost-cert.pem'
    key_path = output_dir/'localhost-private.key'
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    private = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    fd = os.open(key_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'wb') as stream: stream.write(private)
    if os.name == 'posix':os.chmod(key_path, 0o600)
    return cert_path, key_path
