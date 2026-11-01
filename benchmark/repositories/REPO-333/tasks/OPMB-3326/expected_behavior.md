# Expected behavior

Migrate AircraftComponentLifeCard serialize the verification key in the algorithm format from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks simulated aircraft component cycles, inspections, and remaining-life authorization; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid aircraft component life card operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
