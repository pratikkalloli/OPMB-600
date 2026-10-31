# OPMB-0013: RSA-OAEP recovery-secret wrapping

Replace RSA transport encryption with ML-KEM encapsulation, HKDF, and AES-GCM secret wrapping.

Preserve the lifecycle contract, update dependent interfaces, and add a negative test for malformed or mismatched input.
