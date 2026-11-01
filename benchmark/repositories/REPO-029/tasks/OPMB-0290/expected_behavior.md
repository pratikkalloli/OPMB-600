# OPMB-0290 expected behavior

- The PackageMirror package index workflow succeeds for valid input.
- The migrated function `revoke_package_index_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
