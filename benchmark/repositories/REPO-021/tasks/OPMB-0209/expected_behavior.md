# OPMB-0209 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `rotate_mail_envelope_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
