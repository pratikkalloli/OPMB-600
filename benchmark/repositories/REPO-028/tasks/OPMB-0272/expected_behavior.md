# OPMB-0272 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `export_update_release_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
