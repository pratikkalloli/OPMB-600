# OPMB-0224 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `validate_configuration_release` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
