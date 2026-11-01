# OPMB-0308 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `seal_consent_record_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
