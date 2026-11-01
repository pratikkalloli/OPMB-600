# OPMB-0216 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `sign_session_offer` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
