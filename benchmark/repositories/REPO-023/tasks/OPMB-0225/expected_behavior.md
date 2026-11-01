# OPMB-0225 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `canonicalize_configuration_release` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
