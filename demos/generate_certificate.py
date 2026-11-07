"""Run: python -m demos.generate_certificate [ECDSA|RSA]"""
import sys
from pathlib import Path
from crypto_lab.certificates import generate_local_cert

if __name__ == '__main__':
    choice = sys.argv[1].upper() if len(sys.argv)>1 else 'ECDSA'
    cert, key = generate_local_cert(Path('.local'), choice)
    print(f'Generated local self-signed {choice} certificate: {cert}')
    print(f'Generated local PRIVATE key (gitignored): {key}')
