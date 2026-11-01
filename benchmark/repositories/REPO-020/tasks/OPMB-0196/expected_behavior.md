# OPMB-0196 expected behavior

- The TimeSeal timestamp token workflow succeeds for valid input.
- The migrated function `sign_timestamp_token` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
