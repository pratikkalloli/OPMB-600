# SecureBLEPairingBook

Records bluetooth pairing authorization and session expiry for a named embedded device pair.

Workflow: Records bluetooth pairing authorization and session expiry for a named embedded device pair; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_secure_b_l_e_pairing_book.py` and `python -m pytest tests/test_secure_b_l_e_pairing_book_pqc.py` from this directory.
