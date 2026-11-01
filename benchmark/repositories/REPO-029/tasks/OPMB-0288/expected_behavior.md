# OPMB-0288 expected behavior

- The PackageMirror package index workflow succeeds for valid input.
- The migrated function `seal_package_index_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
