# OPMB-0320 expected behavior

- The FleetPermit vehicle permit workflow succeeds for valid input.
- The migrated function `revoke_vehicle_permit_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
