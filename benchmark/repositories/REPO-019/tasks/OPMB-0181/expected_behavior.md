# OPMB-0181 expected behavior

- The WebhookShield delivery workflow succeeds for valid input.
- The migrated function `create_delivery_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
