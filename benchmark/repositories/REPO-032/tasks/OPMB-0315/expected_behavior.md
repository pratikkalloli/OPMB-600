# OPMB-0315 expected behavior

- The FleetPermit vehicle permit workflow succeeds for valid input.
- The migrated function `canonicalize_vehicle_permit` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
