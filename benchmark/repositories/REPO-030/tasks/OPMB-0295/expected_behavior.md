# OPMB-0295 expected behavior

- The ApprovalFlow approval request workflow succeeds for valid input.
- The migrated function `canonicalize_approval_request` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
