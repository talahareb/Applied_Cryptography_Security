"""RSA, Diffie-Hellman and key derivation using the cryptography package."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# ffdhe2048 prime and generator from RFC 7919, supplied in the course Lab 03.
FFDHE2048_P = int(
    'FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF97D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD65612433F51F5F066ED0856365553DED1AF3B557135E7F57C935984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE73530ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FBB96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB190B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F619172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD733BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA886B423861285C97FFFFFFFFFFFFFFFF', 16
)


def generate_rsa_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def rsa_encrypt(public_key, plaintext: bytes) -> bytes:
    return public_key.encrypt(plaintext, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))


def rsa_decrypt(private_key, ciphertext: bytes) -> bytes:
    return private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))


def rsa_sign(private_key, message: bytes) -> bytes:
    return private_key.sign(message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())


def rsa_verify(public_key, signature: bytes, message: bytes) -> None:
    public_key.verify(signature, message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())


def exchange_derived_key() -> tuple[bytes, bytes]:
    """Generate ephemeral DH key pairs and derive 256-bit keys for both parties."""
    params = dh.DHParameterNumbers(FFDHE2048_P, 2).parameters()
    alice = params.generate_private_key()
    bob = params.generate_private_key()
    alice_secret = alice.exchange(bob.public_key())
    bob_secret = bob.exchange(alice.public_key())
    def derive(secret: bytes):
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=b'aisc-demo-fixed-public-salt', info=b'aisc-dh-demo').derive(secret)
    return derive(alice_secret), derive(bob_secret)
