# OPMB-0210 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `revoke_mail_envelope_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
