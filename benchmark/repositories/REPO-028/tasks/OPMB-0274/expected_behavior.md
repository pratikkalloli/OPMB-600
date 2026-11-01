# OPMB-0274 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `validate_update_release` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
