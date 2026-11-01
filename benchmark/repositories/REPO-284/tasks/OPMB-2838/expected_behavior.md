# Expected behavior

Migrate DeviceRecoveryTicket protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Coordinates recovery of a lost device identity and records invalidation of its previous credentials; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid device recovery ticket operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
