# OPMB-0232 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `export_provenance_checkpoint_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
