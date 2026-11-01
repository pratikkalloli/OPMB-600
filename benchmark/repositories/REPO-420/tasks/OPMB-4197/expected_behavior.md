# Expected behavior

Migrate FarmProducePackingLot load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Links harvested produce to packing line, grade result, and shipping destination; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid farm produce packing lot operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
