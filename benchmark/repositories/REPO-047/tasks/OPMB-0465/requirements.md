# OPMB-0465: SecureForms: Generate recipient key pairs

Replace RSA recipient keys with ML-KEM-768 keys without reusing decision-signing keys. SecureForms workflow: Form submissions binding schema version, submitter reference, consent version, and processing lifecycle. Domain-specific invariants: Submission schema version must be positive and consent version must be present. The task concerns fields form_id, submission_id, submitter_ref, schema_version, received_at, consent_version, processing_state and legal transitions received -> validated -> sealed -> rejected.

## Required changes

- Migrate the identified operation to ML-KEM-768.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
