# OPMB-0175 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `canonicalize_zone_update` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
