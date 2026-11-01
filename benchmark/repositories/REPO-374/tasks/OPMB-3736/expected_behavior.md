# Expected behavior

Migrate CarrierInterconnectReceipt serialize the verification key in the algorithm format from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Reconciles carrier interconnect traffic totals and signed settlement acknowledgements; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid carrier interconnect receipt operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
