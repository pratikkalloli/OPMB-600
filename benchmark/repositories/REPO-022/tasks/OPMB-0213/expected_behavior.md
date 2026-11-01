# OPMB-0213 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `load_session_offer_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
