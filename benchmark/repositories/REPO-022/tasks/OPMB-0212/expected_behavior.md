# OPMB-0212 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `export_session_offer_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
