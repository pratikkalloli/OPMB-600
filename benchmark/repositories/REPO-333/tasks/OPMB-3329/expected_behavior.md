# Expected behavior

Migrate AircraftComponentLifeCard recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Tracks simulated aircraft component cycles, inspections, and remaining-life authorization; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid aircraft component life card operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
