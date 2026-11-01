# OPMB-0437: KeyRecovery: Open a protected domain attachment

Migrate envelope opening to ML-KEM decapsulation and preserve rejection of wrong recipients, identifiers, and tampering. KeyRecovery workflow: Threshold recovery cases tracking principal, key fingerprint, required approvals, and fulfillment decisions. Domain-specific invariants: Recovery requires a threshold between two and five distinct approvals. The task concerns fields recovery_id, principal_id, key_fingerprint, approvals_required, opened_at, recovery_state and legal transitions opened -> approved -> fulfilled -> denied.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
