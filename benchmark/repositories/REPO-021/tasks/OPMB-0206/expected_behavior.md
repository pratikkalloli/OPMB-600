# OPMB-0206 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `sign_mail_envelope` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
