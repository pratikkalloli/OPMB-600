# OPMB-0218 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `seal_session_offer_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
