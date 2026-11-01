# OPMB-0270 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `revoke_dispatch_instruction_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
