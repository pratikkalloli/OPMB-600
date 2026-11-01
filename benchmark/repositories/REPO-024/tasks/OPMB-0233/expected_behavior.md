# OPMB-0233 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `load_provenance_checkpoint_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
