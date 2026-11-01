# Expected behavior

Migrate SoilProbeCalibration protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Tracks soil probe calibration factors and service interval for a named field location; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid soil probe calibration operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
