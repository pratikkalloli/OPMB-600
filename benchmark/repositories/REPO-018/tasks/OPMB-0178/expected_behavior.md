# OPMB-0178 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `seal_zone_update_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
