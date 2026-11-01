# OPMB-0313 expected behavior

- The FleetPermit vehicle permit workflow succeeds for valid input.
- The migrated function `load_vehicle_permit_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
