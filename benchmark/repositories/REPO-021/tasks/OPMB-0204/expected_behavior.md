# OPMB-0204 expected behavior

- The MailGuard mail envelope workflow succeeds for valid input.
- The migrated function `validate_mail_envelope` uses Domain-specific input and authorization preconditions.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
