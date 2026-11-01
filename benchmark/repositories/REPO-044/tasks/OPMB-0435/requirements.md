# OPMB-0435: KeyRecovery: Generate recipient key pairs

Replace RSA recipient keys with ML-KEM-768 keys without reusing decision-signing keys. KeyRecovery workflow: Threshold recovery cases tracking principal, key fingerprint, required approvals, and fulfillment decisions. Domain-specific invariants: Recovery requires a threshold between two and five distinct approvals. The task concerns fields recovery_id, principal_id, key_fingerprint, approvals_required, opened_at, recovery_state and legal transitions opened -> approved -> fulfilled -> denied.

## Required changes

- Migrate the identified operation to ML-KEM-768.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
