# OPMB-0191 expected behavior

- The TimeSeal timestamp token workflow succeeds for valid input.
- The migrated function `create_timestamp_token_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
