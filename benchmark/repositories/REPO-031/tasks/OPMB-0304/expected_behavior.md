# OPMB-0304 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `validate_consent_record` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
