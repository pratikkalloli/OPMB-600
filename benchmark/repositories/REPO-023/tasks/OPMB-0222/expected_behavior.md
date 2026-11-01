# OPMB-0222 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `export_configuration_release_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
