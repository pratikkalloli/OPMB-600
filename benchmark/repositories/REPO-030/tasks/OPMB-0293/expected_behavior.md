# OPMB-0293 expected behavior

- The ApprovalFlow approval request workflow succeeds for valid input.
- The migrated function `load_approval_request_public_key` uses Strict ML-DSA/ML-KEM public-key decoding and type validation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
