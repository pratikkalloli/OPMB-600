# OPMB-0179 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `rotate_zone_update_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
