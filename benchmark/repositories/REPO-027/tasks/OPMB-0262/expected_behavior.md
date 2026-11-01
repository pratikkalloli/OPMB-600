# OPMB-0262 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `export_dispatch_instruction_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
