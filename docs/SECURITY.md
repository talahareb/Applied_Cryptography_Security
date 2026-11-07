# Educational security boundaries

The scripts in `demos/` are standalone local experiments, not a deployable security service.

- The HTTPS server listens only on 127.0.0.1; generated private keys are local and ignored by Git.
- The TLS client verifies the server's certificate and localhost name against the locally generated trust certificate.
- AES-CTR provides confidentiality, **not** message authenticity. The companion demo includes AES-GCM for authenticated encryption.
- RSA-OAEP/PSS replace textbook RSA with established padded operations.
- Collision experiments apply only to deliberately truncated (8/16-bit) SHA-256 digests, not full SHA-256.
- The Schnorr attack uses tiny illustrative parameters and is not a real-world key-recovery tool.
- Original coursework scripts are archival references and may contain outdated/insecure classroom settings.
