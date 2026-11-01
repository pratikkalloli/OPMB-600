# OPMB-0237 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `verify_provenance_checkpoint` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
