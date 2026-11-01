# OPMB-0312 expected behavior

- The FleetPermit vehicle permit workflow succeeds for valid input.
- The migrated function `export_vehicle_permit_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
