import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography import x509
from crypto_lab.symmetric import *
from crypto_lab.public_key import *
from crypto_lab.hashing import *
from crypto_lab.toy_schnorr import *
from crypto_lab.certificates import generate_local_cert


class TestCryptographyDemo(unittest.TestCase):
    def test_aes_ctr_roundtrip(self):
        k=os.urandom(16); plain=b'hello world' * 4
        nonce, encrypted=encrypt_aes_ctr(k,plain)
        self.assertEqual(decrypt_aes_ctr(k,nonce,encrypted),plain)

    def test_aes_gcm_authentication(self):
        k=os.urandom(32); nonce, ct=encrypt_aes_gcm(k,b'abc',b'aad')
        self.assertEqual(decrypt_aes_gcm(k,nonce,ct,b'aad'),b'abc')
        with self.assertRaises(InvalidTag):decrypt_aes_gcm(k,nonce,ct,b'wrong-aad')

    def test_rsa_oaep_and_pss(self):
        private=generate_rsa_key();msg=b'cryptography demonstration'
        self.assertEqual(rsa_decrypt(private,rsa_encrypt(private.public_key(),msg)),msg)
        signature=rsa_sign(private,msg)
        rsa_verify(private.public_key(),signature,msg)
        with self.assertRaises(InvalidSignature):rsa_verify(private.public_key(),signature,msg+b'!')

    def test_diffie_hellman(self):
        a,b=exchange_derived_key()
        self.assertEqual(a,b)
        self.assertEqual(len(a),32)

    def test_hash_and_truncation(self):
        self.assertEqual(sha256_hex(b'abc'),hashlib.sha256(b'abc').hexdigest())
        a,b,d,n=find_truncated_collision(1)
        self.assertNotEqual(a,b)
        self.assertEqual(hashlib.sha256(a).hexdigest()[:2],d)
        self.assertEqual(hashlib.sha256(b).hexdigest()[:2],d)

    def test_toy_schnorr_nonce_exposure(self):
        secret=7; pub=pow(G,secret,P)
        s1=sign(secret,3,b'first')
        s2=sign(secret,4,b'second')
        self.assertTrue(verify(pub,b'first',s1))
        self.assertTrue(verify(pub,b'second',s2))
        self.assertEqual(recover_secret_from_consecutive_nonces(s1,s2),secret)

    def test_generate_local_cert(self):
        with tempfile.TemporaryDirectory() as directory:
            cert_path,key_path=generate_local_cert(Path(directory),'ECDSA')
            self.assertTrue(cert_path.is_file() and key_path.is_file())
            c=x509.load_pem_x509_certificate(cert_path.read_bytes())
            self.assertEqual(c.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value,'localhost')
            self.assertTrue(c.not_valid_after_utc>c.not_valid_before_utc)


if __name__=='__main__':unittest.main()
