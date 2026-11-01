# OPMB-0244 expected behavior

- The MediaRights rights manifest workflow succeeds for valid input.
- The migrated function `validate_rights_manifest` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
