# OPMB-0286 expected behavior

- The PackageMirror package index workflow succeeds for valid input.
- The migrated function `sign_package_index` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
