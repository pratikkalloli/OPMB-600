# Expected behavior

Migrate ToolChangeAuthorization serialize the verification key in the algorithm format from ECDSA P-256/SHA-256 to ML-DSA-65, retaining Tool wear report, technician assignment, supervisor authorization, change confirmation, and return-to-service. semantics.

Valid tool change operations remain interoperable with the documented PQC format. Invalid state, bad tool_serial, altered content, wrong keys, and unsupported versions are rejected.
