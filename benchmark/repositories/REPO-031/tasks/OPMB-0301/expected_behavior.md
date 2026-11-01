# OPMB-0301 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `create_consent_record_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
