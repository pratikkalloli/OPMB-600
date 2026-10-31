# OPMB-0015: RSA signing-key generation

Move audit signer generation to ML-DSA and retain separation from transport keys.

Preserve the lifecycle contract, update dependent interfaces, and add a negative test for malformed or mismatched input.
