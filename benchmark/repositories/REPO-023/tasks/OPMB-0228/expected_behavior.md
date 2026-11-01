# OPMB-0228 expected behavior

- The ConfigSign configuration release workflow succeeds for valid input.
- The migrated function `seal_configuration_release_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
