# OPMB-0282 expected behavior

- The PackageMirror package index workflow succeeds for valid input.
- The migrated function `export_package_index_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
