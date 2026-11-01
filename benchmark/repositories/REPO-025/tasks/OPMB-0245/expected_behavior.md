# OPMB-0245 expected behavior

- The MediaRights rights manifest workflow succeeds for valid input.
- The migrated function `canonicalize_rights_manifest` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
