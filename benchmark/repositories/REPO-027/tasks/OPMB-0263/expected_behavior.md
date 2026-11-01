# OPMB-0263 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `load_dispatch_instruction_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
