# OPMB-0250 expected behavior

- The MediaRights rights manifest workflow succeeds for valid input.
- The migrated function `revoke_rights_manifest_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
