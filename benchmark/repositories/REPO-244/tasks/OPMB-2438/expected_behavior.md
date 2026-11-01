# Expected behavior

Migrate WeldProcedureRelease protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Procedure drafting, welding-engineer qualification, controlled issue, and supersession of a weld specification. semantics.

Valid weld procedure operations remain interoperable with the documented PQC format. Invalid state, bad procedure_digest, altered content, wrong keys, and unsupported versions are rejected.
