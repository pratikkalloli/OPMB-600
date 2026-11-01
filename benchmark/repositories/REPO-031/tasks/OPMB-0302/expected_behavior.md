# OPMB-0302 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `export_consent_record_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
