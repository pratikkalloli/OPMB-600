# OPMB-0171 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `create_zone_update_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
