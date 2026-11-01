# Expected behavior

Migrate TaxiShiftSettlement load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Closes a synthetic taxi shift with trip totals, adjustments, and driver acknowledgement; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid taxi shift settlement operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
