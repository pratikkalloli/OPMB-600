# OPMB-0217 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `verify_session_offer` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
