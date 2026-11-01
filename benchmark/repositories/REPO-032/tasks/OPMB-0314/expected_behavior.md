# OPMB-0314 expected behavior

- The FleetPermit vehicle permit workflow succeeds for valid input.
- The migrated function `validate_vehicle_permit` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
