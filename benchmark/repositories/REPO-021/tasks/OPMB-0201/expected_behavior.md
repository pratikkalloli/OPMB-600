# OPMB-0201 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `create_mail_envelope_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
