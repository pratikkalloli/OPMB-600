# OPMB-0251 expected behavior

- The SecureSurvey survey submission workflow succeeds for valid input.
- The migrated function `create_survey_submission_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
