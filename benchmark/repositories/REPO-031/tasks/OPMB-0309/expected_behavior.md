# OPMB-0309 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `rotate_consent_record_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
