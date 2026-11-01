# OPMB-0248 expected behavior

- The MediaRights rights manifest workflow succeeds for valid input.
- The migrated function `seal_rights_manifest_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
