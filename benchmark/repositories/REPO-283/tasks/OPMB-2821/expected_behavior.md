# Expected behavior

Migrate RemoteProbeRegistry validate the domain record and its lifecycle state from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Registers diagnostic probes, their allowed command set, and the evidence collected from a device; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid remote probe registry operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
