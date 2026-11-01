# OPMB-0264 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `validate_dispatch_instruction` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
