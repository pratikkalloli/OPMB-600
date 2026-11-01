# OPMB-0296 expected behavior

- The ApprovalFlow approval request workflow succeeds for valid input.
- The migrated function `sign_approval_request` uses Context-bound ML-DSA-65 signature over the canonical record.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
