# Expected behavior

Migrate WeldProcedureRelease serialize the verification key in the algorithm format from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Procedure drafting, welding-engineer qualification, controlled issue, and supersession of a weld specification. semantics.

Valid weld procedure operations remain interoperable with the documented PQC format. Invalid state, bad procedure_digest, altered content, wrong keys, and unsupported versions are rejected.
