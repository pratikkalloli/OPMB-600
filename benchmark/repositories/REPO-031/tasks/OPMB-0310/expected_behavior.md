# OPMB-0310 expected behavior

- The ClinicalConsent consent record workflow succeeds for valid input.
- The migrated function `revoke_consent_record_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
