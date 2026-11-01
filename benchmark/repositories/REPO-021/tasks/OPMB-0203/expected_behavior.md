# OPMB-0203 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `load_mail_envelope_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
