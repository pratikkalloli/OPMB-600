# OPMB-0231 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `create_provenance_checkpoint_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
