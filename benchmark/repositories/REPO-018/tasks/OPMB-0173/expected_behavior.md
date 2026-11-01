# OPMB-0173 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `load_zone_update_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
