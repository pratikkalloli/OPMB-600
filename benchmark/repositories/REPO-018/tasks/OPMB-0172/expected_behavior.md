# OPMB-0172 expected behavior

- The DNSZoneGuard zone update workflow succeeds for valid input.
- The migrated function `export_zone_update_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
