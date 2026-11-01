# OPMB-0177 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `verify_zone_update` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
