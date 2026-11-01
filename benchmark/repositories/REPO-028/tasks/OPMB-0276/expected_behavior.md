# OPMB-0276 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `sign_update_release` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
