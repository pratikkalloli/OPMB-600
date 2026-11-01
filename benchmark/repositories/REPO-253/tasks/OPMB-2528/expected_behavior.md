# Expected behavior

Migrate ToolWearForecastCase protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Records measured cutting-tool wear and the maintenance disposition used to prevent an expired tool from returning to a workcell; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid tool wear forecast case operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
