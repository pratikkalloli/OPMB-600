# OPMB-0266 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `sign_dispatch_instruction` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
