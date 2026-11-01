# OPMB-0202 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `export_mail_envelope_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
