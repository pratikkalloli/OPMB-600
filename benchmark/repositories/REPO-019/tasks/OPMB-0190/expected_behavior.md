# OPMB-0190 expected behavior

- The WebhookShield delivery workflow succeeds for valid input.
- The migrated function `revoke_delivery_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
