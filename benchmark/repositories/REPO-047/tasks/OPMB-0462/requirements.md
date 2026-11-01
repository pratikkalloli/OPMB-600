# OPMB-0462: SecureForms: Generate the decision signing key pair

Replace RSA decision-signing keys with ML-DSA-65 keys and keep them separate from recipient key-establishment keys. SecureForms workflow: Form submissions binding schema version, submitter reference, consent version, and processing lifecycle. Domain-specific invariants: Submission schema version must be positive and consent version must be present. The task concerns fields form_id, submission_id, submitter_ref, schema_version, received_at, consent_version, processing_state and legal transitions received -> validated -> sealed -> rejected.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
