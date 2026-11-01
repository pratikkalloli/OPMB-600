# OPMB-0189 expected behavior

- The WebhookShield delivery workflow succeeds for valid input.
- The migrated function `rotate_delivery_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
