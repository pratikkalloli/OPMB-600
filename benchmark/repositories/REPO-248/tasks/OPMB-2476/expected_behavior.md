# Expected behavior

Migrate ProductionDeviationCase serialize the verification key in the algorithm format from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Deviation intake, severity assignment, containment, disposition approval, and closure evidence. semantics.

Valid production deviation operations remain interoperable with the documented PQC format. Invalid state, bad severity, altered content, wrong keys, and unsupported versions are rejected.
