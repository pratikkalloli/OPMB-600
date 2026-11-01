# OPMB-0256 expected behavior

- The SecureSurvey survey submission workflow succeeds for valid input.
- The migrated function `sign_survey_submission` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
