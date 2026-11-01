# OPMB-0268 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `seal_dispatch_instruction_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
