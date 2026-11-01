# OPMB-0281 expected behavior

- The PackageMirror package index workflow succeeds for valid input.
- The migrated function `create_package_index_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
