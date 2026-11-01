# OPMB-0214 expected behavior

- The SessionExchange session offer workflow succeeds for valid input.
- The migrated function `validate_session_offer` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
