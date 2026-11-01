# OPMB-0241 expected behavior

- The MediaRights rights manifest workflow succeeds for valid input.
- The migrated function `create_rights_manifest_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
