# OPMB-0207 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `verify_mail_envelope` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
