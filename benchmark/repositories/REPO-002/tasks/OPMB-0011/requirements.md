# OPMB-0011: RSA-PSS audit event signing

Replace audit-event RSA-PSS signing with ML-DSA-65 while preserving canonical event encoding.

Preserve the lifecycle contract, update dependent interfaces, and add a negative test for malformed or mismatched input.
