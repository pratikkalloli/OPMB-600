# OPMB-0220 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `revoke_session_offer_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
