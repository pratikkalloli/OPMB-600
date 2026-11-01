# Expected behavior

Migrate PacketBrokerFilterUpdate apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Releases a packet broker filter revision with scope and rollback constraints; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid packet broker filter update operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
