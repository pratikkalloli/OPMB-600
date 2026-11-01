# OPMB-0289 expected behavior

- The PackageMirror package index workflow succeeds for valid input.
- The migrated function `rotate_package_index_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
