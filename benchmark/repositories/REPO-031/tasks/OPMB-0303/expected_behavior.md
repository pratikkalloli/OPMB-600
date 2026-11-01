# OPMB-0303 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `load_consent_record_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
