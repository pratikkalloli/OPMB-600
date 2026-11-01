# OPMB-0255 expected behavior

- The SecureSurvey survey submission workflow succeeds for valid input.
- The migrated function `canonicalize_survey_submission` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
