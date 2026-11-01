# OPMB-0187 expected behavior

- The WebhookShield delivery workflow succeeds for valid input.
- The migrated function `verify_delivery` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
