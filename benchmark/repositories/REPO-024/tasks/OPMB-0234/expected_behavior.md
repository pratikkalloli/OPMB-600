# OPMB-0234 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `validate_provenance_checkpoint` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
