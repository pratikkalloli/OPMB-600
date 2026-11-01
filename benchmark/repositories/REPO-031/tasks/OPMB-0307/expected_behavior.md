# OPMB-0307 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `verify_consent_record` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
