# OPMB-0317 expected behavior

- The FleetPermit vehicle permit workflow succeeds for valid input.
- The migrated function `verify_vehicle_permit` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
