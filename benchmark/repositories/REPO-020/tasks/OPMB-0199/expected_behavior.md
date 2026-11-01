# OPMB-0199 expected behavior

- The TimeSeal timestamp token workflow succeeds for valid input.
- The migrated function `rotate_timestamp_token_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
