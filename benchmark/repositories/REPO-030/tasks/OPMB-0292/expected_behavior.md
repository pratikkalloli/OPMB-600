# OPMB-0292 expected behavior

- The ApprovalFlow approval request workflow succeeds for valid input.
- The migrated function `export_approval_request_public_key` uses Versioned DER SubjectPublicKeyInfo encoding with purpose separation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
