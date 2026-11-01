# OPMB-0229 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `rotate_configuration_release_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
