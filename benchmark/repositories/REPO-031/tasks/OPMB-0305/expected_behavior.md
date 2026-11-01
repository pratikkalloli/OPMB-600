# OPMB-0305 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `canonicalize_consent_record` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
