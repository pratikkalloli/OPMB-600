# OPMB-0291 expected behavior

- The ApprovalFlow approval request workflow succeeds for valid input.
- The migrated function `create_approval_request_identity` uses ML-DSA-65 signing and ML-KEM-768 transport key generation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
