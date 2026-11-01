# OPMB-0300 expected behavior

- The ApprovalFlow approval request workflow succeeds for valid input.
- The migrated function `revoke_approval_request_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
