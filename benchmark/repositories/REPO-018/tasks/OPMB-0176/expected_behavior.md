# OPMB-0176 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `sign_zone_update` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
