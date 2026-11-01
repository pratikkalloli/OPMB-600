# Expected behavior

Migrate MachineGuardInspection apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records machine-guard inspection findings and prevents restart until safety-critical findings are closed; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid machine guard inspection operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
