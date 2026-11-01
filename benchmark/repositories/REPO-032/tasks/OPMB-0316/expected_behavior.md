# OPMB-0316 expected behavior

- The FleetPermit vehicle permit workflow succeeds for valid input.
- The migrated function `sign_vehicle_permit` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
