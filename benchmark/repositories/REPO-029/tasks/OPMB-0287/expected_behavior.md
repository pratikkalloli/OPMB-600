# OPMB-0287 expected behavior

- The PackageMirror package index workflow succeeds for valid input.
- The migrated function `verify_package_index` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
