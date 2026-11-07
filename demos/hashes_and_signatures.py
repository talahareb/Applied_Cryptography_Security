"""Run: python -m demos.hashes_and_signatures"""
from crypto_lab.hashing import sha256_hex, find_truncated_collision
from crypto_lab.toy_schnorr import G, P, Q, sign, verify, recover_secret_from_consecutive_nonces


def main():
    msg = b'Applied Cryptography course demo'
    print('SHA-256:', sha256_hex(msg))
    m1, m2, short_digest, count = find_truncated_collision(2)
    assert m1 != m2
    print(f'Truncated SHA-256 (16 bits): digest {short_digest} collides after {count} samples')
    secret, k1 = 7, 3
    public = pow(G, secret, P)
    msg1, msg2 = b'lab message one', b'lab message two'
    sig1 = sign(secret, k1, msg1)
    sig2 = sign(secret, k1 + 1, msg2)
    assert verify(public, msg1, sig1) and verify(public, msg2, sig2)
    recovered = recover_secret_from_consecutive_nonces(sig1, sig2)
    assert recovered == secret
    print(f'Toy Schnorr: consecutive nonces reveal the signing key ({recovered} in mod-{Q} group)')
    print('The tiny Schnorr example and truncated digest are educational only.')


if __name__ == '__main__':
    main()
