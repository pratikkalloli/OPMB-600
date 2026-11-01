# OPMB-0285 expected behavior

- The PackageMirror package index workflow succeeds for valid input.
- The migrated function `canonicalize_package_index` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
