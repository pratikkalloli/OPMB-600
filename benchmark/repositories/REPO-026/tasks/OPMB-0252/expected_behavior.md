# OPMB-0252 expected behavior

- The SecureSurvey survey submission workflow succeeds for valid input.
- The migrated function `export_survey_submission_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
