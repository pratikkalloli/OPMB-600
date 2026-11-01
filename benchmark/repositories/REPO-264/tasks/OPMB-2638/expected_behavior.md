# Expected behavior

Migrate WorkOrderTraveler protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Carries a serialized work order through required operations and captures station-level signoff; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid work order traveler operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
