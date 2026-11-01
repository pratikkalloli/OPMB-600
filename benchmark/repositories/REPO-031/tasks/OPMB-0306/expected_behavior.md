# OPMB-0306 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `sign_consent_record` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
