"""Run: python -m demos.encryption_and_key_exchange"""
import os
from crypto_lab.symmetric import encrypt_aes_ctr, decrypt_aes_ctr, encrypt_aes_gcm, decrypt_aes_gcm
from crypto_lab.public_key import generate_rsa_key, rsa_encrypt, rsa_decrypt, rsa_sign, rsa_verify, exchange_derived_key


def main():
    message = b'Applied Cryptography course demo'
    key = os.urandom(32)
    ctr_nonce, ctr_ciphertext = encrypt_aes_ctr(key, message)
    assert decrypt_aes_ctr(key, ctr_nonce, ctr_ciphertext) == message
    print('[AES-CTR] Encrypt/decrypt passed (confidentiality only; no integrity)')

    gcm_nonce, gcm_ciphertext = encrypt_aes_gcm(key, message)
    assert decrypt_aes_gcm(key, gcm_nonce, gcm_ciphertext) == message
    print('[AES-GCM] Authenticated encrypt/decrypt passed')

    private = generate_rsa_key()
    ciphertext = rsa_encrypt(private.public_key(), message)
    assert rsa_decrypt(private, ciphertext) == message
    signature = rsa_sign(private, message)
    rsa_verify(private.public_key(), signature, message)
    print('[RSA] OAEP encryption and PSS signature verification passed')

    alice_key, bob_key = exchange_derived_key()
    assert alice_key == bob_key
    nonce, payload = encrypt_aes_gcm(alice_key, message)
    assert decrypt_aes_gcm(bob_key, nonce, payload) == message
    print('[DH + HKDF + AES-GCM] Both parties derived the same session key')


if __name__ == '__main__':
    main()
