# OPMB-0182 expected behavior

- The WebhookShield delivery workflow succeeds for valid input.
- The migrated function `export_delivery_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
