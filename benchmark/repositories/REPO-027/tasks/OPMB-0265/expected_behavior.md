# OPMB-0265 expected behavior

- The GeoDispatch dispatch instruction workflow succeeds for valid input.
- The migrated function `canonicalize_dispatch_instruction` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
