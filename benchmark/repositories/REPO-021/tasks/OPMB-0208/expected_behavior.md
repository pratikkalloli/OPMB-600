# OPMB-0208 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `seal_mail_envelope_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
