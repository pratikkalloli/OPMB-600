# OPMB-0200 expected behavior

- The TimeSeal timestamp token workflow succeeds for valid input.
- The migrated function `revoke_timestamp_token_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
