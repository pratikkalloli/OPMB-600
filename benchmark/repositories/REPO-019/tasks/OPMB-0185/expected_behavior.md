# OPMB-0185 expected behavior

- The WebhookShield delivery workflow succeeds for valid input.
- The migrated function `canonicalize_delivery` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
