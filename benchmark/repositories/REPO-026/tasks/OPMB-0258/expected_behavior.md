# OPMB-0258 expected behavior

- The SecureSurvey survey submission workflow succeeds for valid input.
- The migrated function `seal_survey_submission_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
