# Expected behavior

Migrate ToolWearForecastCase sign a scoped domain record with versioned context from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records measured cutting-tool wear and the maintenance disposition used to prevent an expired tool from returning to a workcell; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid tool wear forecast case operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
