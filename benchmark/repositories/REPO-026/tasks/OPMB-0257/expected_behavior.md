# OPMB-0257 expected behavior

- The SecureSurvey survey submission workflow succeeds for valid input.
- The migrated function `verify_survey_submission` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
