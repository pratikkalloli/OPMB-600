# OPMB-0283 expected behavior

- The PackageMirror package index workflow succeeds for valid input.
- The migrated function `load_package_index_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
