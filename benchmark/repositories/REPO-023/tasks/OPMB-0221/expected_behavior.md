# OPMB-0221 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `create_configuration_release_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
