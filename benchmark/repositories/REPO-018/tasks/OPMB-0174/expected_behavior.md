# OPMB-0174 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `validate_zone_update` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
