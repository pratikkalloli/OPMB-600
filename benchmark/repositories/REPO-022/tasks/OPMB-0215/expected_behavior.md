# OPMB-0215 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `canonicalize_session_offer` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
