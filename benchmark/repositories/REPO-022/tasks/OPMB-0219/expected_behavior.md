# OPMB-0219 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `rotate_session_offer_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
