# OPMB-0271 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `create_update_release_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
