# OPMB-0186 expected behavior

- The WebhookShield delivery workflow succeeds for valid input.
- The migrated function `sign_delivery` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
