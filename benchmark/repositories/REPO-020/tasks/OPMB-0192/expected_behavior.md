# OPMB-0192 expected behavior

- The TimeSeal timestamp token workflow succeeds for valid input.
- The migrated function `export_timestamp_token_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
