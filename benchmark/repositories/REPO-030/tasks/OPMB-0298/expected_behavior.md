# OPMB-0298 expected behavior

- The ApprovalFlow approval request workflow succeeds for valid input.
- The migrated function `seal_approval_request_payload` uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
