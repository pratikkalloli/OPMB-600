# OPMB-0205 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `canonicalize_mail_envelope` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
