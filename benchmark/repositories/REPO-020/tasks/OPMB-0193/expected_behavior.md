# OPMB-0193 expected behavior

- The TimeSeal timestamp token workflow succeeds for valid input.
- The migrated function `load_timestamp_token_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
