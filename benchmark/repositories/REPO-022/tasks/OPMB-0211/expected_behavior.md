# OPMB-0211 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `create_session_offer_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
