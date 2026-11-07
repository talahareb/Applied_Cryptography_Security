"""Small-number Schnorr-style signatures illustrating consecutive-nonce leakage.

These parameters are deliberately tiny; the demonstration is for mathematics only.
"""
import hashlib

P, Q, G = 23, 11, 2  # G has order Q modulo P


def challenge(r: int, message: bytes) -> int:
    return int.from_bytes(hashlib.sha256(str(r).encode() + b'|' + message).digest(), 'big') % Q


def sign(secret: int, nonce: int, message: bytes):
    r = pow(G, nonce, P)
    e = challenge(r, message)
    s = (nonce - e * secret) % Q
    return (r, e, s)


def verify(public_key: int, message: bytes, signature: tuple[int,int,int]) -> bool:
    r, e, s = signature
    return e == challenge(r, message) and (pow(G, s, P) * pow(public_key, e, P)) % P == r


def recover_secret_from_consecutive_nonces(sig1, sig2):
    _, e1, s1 = sig1
    _, e2, s2 = sig2
    d = (e1 - e2) % Q
    if d == 0:
        raise ValueError('Choose messages giving different challenges')
    return ((s2 - s1 - 1) * pow(d, -1, Q)) % Q
