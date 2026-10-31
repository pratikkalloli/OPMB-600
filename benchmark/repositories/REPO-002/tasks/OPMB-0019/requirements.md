# OPMB-0019: Private-key restoration interface

Update private-key loading to support encrypted PKCS#8 ML-KEM/ML-DSA objects and reject classical fallback.

Preserve the lifecycle contract, update dependent interfaces, and add a negative test for malformed or mismatched input.
