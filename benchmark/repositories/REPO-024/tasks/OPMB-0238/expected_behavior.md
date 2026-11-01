# OPMB-0238 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `seal_provenance_checkpoint_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
