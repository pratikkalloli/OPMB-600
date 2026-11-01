# Expected behavior

Migrate RoboticsSafetyEnvelope load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Sets the approved motion limits and emergency-stop profile for a robot operating mode; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid robotics safety envelope operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
