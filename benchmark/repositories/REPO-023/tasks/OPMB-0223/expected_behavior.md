# OPMB-0223 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `load_configuration_release_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
