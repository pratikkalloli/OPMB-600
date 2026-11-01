# OPMB-0247 expected behavior

- The MediaRights rights manifest workflow succeeds for valid input.
- The migrated function `verify_rights_manifest` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
