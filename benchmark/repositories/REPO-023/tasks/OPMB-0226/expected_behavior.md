# OPMB-0226 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `sign_configuration_release` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
