# OPMB-0297 expected behavior

- The ApprovalFlow approval request workflow succeeds for valid input.
- The migrated function `verify_approval_request` uses ML-DSA verification with tamper and context rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
