# OPMB-0277 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `verify_update_release` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
