# TorqueAuditLedger

Retains signed torque-tool readings against a production job so quality staff can reconcile out-of-tolerance fastening events.

Workflow: Retains signed torque-tool readings against a production job so quality staff can reconcile out-of-tolerance fastening events; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_torque_audit_ledger.py` and `python -m pytest tests/test_torque_audit_ledger_pqc.py` from this directory.

## Domain workflow

Both the original and PQC services implement `reconcile_torque_readings`. It enforces the application's stated business rule and records the decision with the signed record's workflow event.
