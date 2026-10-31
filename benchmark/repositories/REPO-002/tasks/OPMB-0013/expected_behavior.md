# Expected behavior

Replace RSA transport encryption with ML-KEM encapsulation, HKDF, and AES-GCM secret wrapping. The inventory continues to represent lifecycle state correctly and cryptographic failures do not expose key material.
