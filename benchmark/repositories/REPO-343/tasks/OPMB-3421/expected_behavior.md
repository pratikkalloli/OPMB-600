# Expected behavior

Migrate AircraftGroundPowerLog validate the domain record and its lifecycle state from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records ground power connection intervals and inspection before aircraft dispatch; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid aircraft ground power log operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
