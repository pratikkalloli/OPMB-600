# OPMB-0468: SecureForms: Encode recipient public-key material

Replace RSA PEM serialization with the pinned provider raw ML-KEM-768 public-key encoding and update consumers. SecureForms workflow: Form submissions binding schema version, submitter reference, consent version, and processing lifecycle. Domain-specific invariants: Submission schema version must be positive and consent version must be present. The task concerns fields form_id, submission_id, submitter_ref, schema_version, received_at, consent_version, processing_state and legal transitions received -> validated -> sealed -> rejected.

## Required changes

- Migrate the identified operation to ML-KEM-768.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
