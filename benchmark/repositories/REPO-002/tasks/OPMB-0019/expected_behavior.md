# Expected behavior

Update private-key loading to support encrypted PKCS#8 ML-KEM/ML-DSA objects and reject classical fallback. The inventory continues to represent lifecycle state correctly and cryptographic failures do not expose key material.
