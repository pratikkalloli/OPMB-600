# OPMB-0227 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `verify_configuration_release` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
