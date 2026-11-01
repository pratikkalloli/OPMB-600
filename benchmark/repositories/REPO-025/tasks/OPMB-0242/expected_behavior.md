# OPMB-0242 expected behavior

- The MediaRights rights manifest workflow succeeds for valid input.
- The migrated function `export_rights_manifest_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
