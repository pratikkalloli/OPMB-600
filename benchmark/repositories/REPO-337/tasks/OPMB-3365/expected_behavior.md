# Expected behavior

Migrate BusDepotChargeDispatch verify a record signature and reject changed records from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Schedules bus charging against departure readiness, charger availability, and energy limits; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid bus depot charge dispatch operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
