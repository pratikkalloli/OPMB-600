# OPMB-0246 expected behavior

- The MediaRights rights manifest workflow succeeds for valid input.
- The migrated function `sign_rights_manifest` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
