# OPMB-0469: SecureForms: Rotate an attachment recipient

Rewrap attachment data keys for a replacement ML-KEM recipient without changing the protected payload or entity context. SecureForms workflow: Form submissions binding schema version, submitter reference, consent version, and processing lifecycle. Domain-specific invariants: Submission schema version must be positive and consent version must be present. The task concerns fields form_id, submission_id, submitter_ref, schema_version, received_at, consent_version, processing_state and legal transitions received -> validated -> sealed -> rejected.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
