# OPMB-0253 expected behavior

- The SecureSurvey survey submission workflow succeeds for valid input.
- The migrated function `load_survey_submission_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
