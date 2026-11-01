# OPMB-0236 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `sign_provenance_checkpoint` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
