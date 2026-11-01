# OPMB-0279 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `rotate_update_release_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
