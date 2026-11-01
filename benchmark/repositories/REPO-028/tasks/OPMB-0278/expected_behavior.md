# OPMB-0278 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `seal_update_release_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
