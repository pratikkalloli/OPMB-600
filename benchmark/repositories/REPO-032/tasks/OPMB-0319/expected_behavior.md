# OPMB-0319 expected behavior

- The FleetPermit vehicle permit workflow succeeds for valid input.
- The migrated function `rotate_vehicle_permit_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
