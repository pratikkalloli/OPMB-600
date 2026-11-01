# OPMB-0026: Print-job key decapsulation and authenticated decryption

Decapsulate the ML-KEM secret, derive the same job-scoped key, and reject malformed encapsulations or modified ciphertext.

Target: ML-KEM-768, HKDF-SHA-256, AES-256-GCM.
