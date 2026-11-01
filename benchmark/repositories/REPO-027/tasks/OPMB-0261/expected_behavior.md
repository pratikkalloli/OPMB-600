# OPMB-0261 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `create_dispatch_instruction_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
