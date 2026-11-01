# OPMB-0273 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `load_update_release_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
