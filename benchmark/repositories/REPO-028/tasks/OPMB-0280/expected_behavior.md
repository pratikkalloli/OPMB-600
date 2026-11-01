# OPMB-0280 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `revoke_update_release_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
