# SerializedMachinePassport

Tracks an industrial machine's identity, custodian, and maintenance attestations across controlled ownership changes.

Workflow: Tracks an industrial machine's identity, custodian, and maintenance attestations across controlled ownership changes; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_serialized_machine_passport.py` and `python -m pytest tests/test_serialized_machine_passport_pqc.py` from this directory.

## Domain workflow

Both the original and PQC services implement `transfer_machine_custody`. It enforces the application's stated business rule and records the decision with the signed record's workflow event.
