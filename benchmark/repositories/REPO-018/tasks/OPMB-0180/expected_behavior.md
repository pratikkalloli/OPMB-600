# OPMB-0180 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `revoke_zone_update_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
