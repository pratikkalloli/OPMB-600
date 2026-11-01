# OPMB-0269 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `rotate_dispatch_instruction_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
