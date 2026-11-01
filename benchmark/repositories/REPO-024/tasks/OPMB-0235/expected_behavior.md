# OPMB-0235 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `canonicalize_provenance_checkpoint` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
