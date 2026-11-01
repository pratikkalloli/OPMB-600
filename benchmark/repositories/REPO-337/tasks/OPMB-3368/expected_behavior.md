# Expected behavior

Migrate BusDepotChargeDispatch protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Schedules bus charging against departure readiness, charger availability, and energy limits; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid bus depot charge dispatch operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
