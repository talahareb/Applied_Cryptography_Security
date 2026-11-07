"""AES-CTR (course topic) and authenticated AES-GCM (modern companion)."""
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_aes_ctr(key: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
    """Return a fresh 16-byte counter block and ciphertext. CTR has NO authenticity."""
    nonce = os.urandom(16)
    encryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    return nonce, encryptor.update(plaintext) + encryptor.finalize()


def decrypt_aes_ctr(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    decryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def encrypt_aes_gcm(key: bytes, plaintext: bytes, aad: bytes = b"") -> tuple[bytes, bytes]:
    nonce = os.urandom(12)
    return nonce, AESGCM(key).encrypt(nonce, plaintext, aad)


def decrypt_aes_gcm(key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes = b"") -> bytes:
    return AESGCM(key).decrypt(nonce, ciphertext, aad)
