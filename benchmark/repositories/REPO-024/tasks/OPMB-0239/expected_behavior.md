# OPMB-0239 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `rotate_provenance_checkpoint_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
