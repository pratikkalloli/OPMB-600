# OPMB-0197 expected behavior

- The TimeSeal timestamp token workflow succeeds for valid input.
- The migrated function `verify_timestamp_token` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
