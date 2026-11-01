# OPMB-0183 expected behavior

- The WebhookShield delivery workflow succeeds for valid input.
- The migrated function `load_delivery_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
