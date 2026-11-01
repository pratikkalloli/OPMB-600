# OPMB-0249 expected behavior

- The MediaRights rights manifest workflow succeeds for valid input.
- The migrated function `rotate_rights_manifest_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
