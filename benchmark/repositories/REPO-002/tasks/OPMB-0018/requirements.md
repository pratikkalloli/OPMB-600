# OPMB-0018: Encrypted private-key persistence format

Migrate protected private-key export to provider-supported encrypted PKCS#8 for PQC key material.

Preserve the lifecycle contract, update dependent interfaces, and add a negative test for malformed or mismatched input.
