# OPMB-0198 expected behavior

- The TimeSeal timestamp token workflow succeeds for valid input.
- The migrated function `seal_timestamp_token_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
