# Original coursework & implementation map

**Course:** Applied Information Security and Cryptography (AISC), Politecnico di Torino, 2025.  
**Author:** Tala Hareb; course starter scripts were supplied in the original labs.

The original, unmodified classroom Python scripts are available under `coursework_original/`, with their folder names preserved. They document the progression from an AES-CTR/RSA/DH worksheet through hash arithmetic and local HTTPS/TLS. The public-facing `crypto_lab/` and `demos/` folders are **companion implementations written for this repository** using current cryptography APIs; they are not represented as code that was included in the original submissions.

| Topic | Course evidence | Executable in this repository |
|---|---|---|
| AES-CTR | Lab 03 original Python source | AES-CTR plus AES-GCM companion demo |
| RSA, finite-field DH | Lab 03 report experiments; starter source provided DH group and prime utilities | RSA-OAEP/RSA-PSS and ephemeral FFDHE2048 + HKDF companion demo |
| SHA-256 and modular arithmetic | Lab 04 original Python source | Truncated-digest collision experiment |
| Schnorr weakness | Lab 04 report described predictable/related signature nonces | Separate, clearly labeled toy Schnorr demonstration |
| Certificates, local HTTPS, TLS inspection | Lab 05 original Python sources | Updated localhost-only HTTPS server/client and certificate generator |

Original lab `Instructions.pdf` files are not redistributed. Reports are also omitted because they include personal/instructor key values and classroom-specific details. Historical scripts in `coursework_original/` may contain deliberately weak examples or outdated TLS settings; run the modern `demos/` programs instead.

The original Lab 03 `text.txt`, old sample trust certificates, and course-specific certificate PEM were also left out. No original private key files are shipped.
