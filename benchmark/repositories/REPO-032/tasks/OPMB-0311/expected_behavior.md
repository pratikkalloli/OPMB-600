# OPMB-0311 expected behavior

- The FleetPermit vehicle permit workflow succeeds for valid input.
- The migrated function `create_vehicle_permit_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
