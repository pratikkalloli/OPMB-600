# OPMB-0230 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `revoke_configuration_release_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
