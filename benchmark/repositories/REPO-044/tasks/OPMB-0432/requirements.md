# OPMB-0432: KeyRecovery: Generate the decision signing key pair

Replace RSA decision-signing keys with ML-DSA-65 keys and keep them separate from recipient key-establishment keys. KeyRecovery workflow: Threshold recovery cases tracking principal, key fingerprint, required approvals, and fulfillment decisions. Domain-specific invariants: Recovery requires a threshold between two and five distinct approvals. The task concerns fields recovery_id, principal_id, key_fingerprint, approvals_required, opened_at, recovery_state and legal transitions opened -> approved -> fulfilled -> denied.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
