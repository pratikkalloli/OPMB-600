# Expected behavior

Migrate AirportBaggageCustody apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks baggage custody scans between check-in, transfer, and reclaim points; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid airport baggage custody operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
