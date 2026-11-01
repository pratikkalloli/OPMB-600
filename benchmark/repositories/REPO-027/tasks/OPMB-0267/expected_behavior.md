# OPMB-0267 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `verify_dispatch_instruction` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
