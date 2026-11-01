# OPMB-0299 expected behavior

- The ApprovalFlow approval request workflow succeeds for valid input.
- The migrated function `rotate_approval_request_identity` uses Versioned signing and transport key rotation.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
