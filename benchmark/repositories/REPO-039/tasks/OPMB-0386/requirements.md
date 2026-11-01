# OPMB-0386: SecureQueue: Seal a protected domain attachment

Replace RSA-OAEP data-key wrapping with ML-KEM-derived wrapping keys and AES-GCM, bound to the entity identifier. SecureQueue workflow: Queue message delivery receipts with producer identity, lease expiry, acknowledgement, and dead-letter state. Domain-specific invariants: A queue message must expire after creation to avoid immediately invalid leases. The task concerns fields message_id, queue_name, producer_id, created_at, expires_at, delivery_state and legal transitions pending -> leased -> acked -> dead_letter.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
