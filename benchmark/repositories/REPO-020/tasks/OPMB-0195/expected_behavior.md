# OPMB-0195 expected behavior

- The TimeSeal timestamp token workflow succeeds for valid input.
- The migrated function `canonicalize_timestamp_token` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
