# ProductionDeviationCase

Routes manufacturing deviations through severity-based containment and disposition, preserving the approver trail for each corrective decision.

Workflow: Deviation intake, severity assignment, containment, disposition approval, and closure evidence.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_production_deviation_case.py` and `python -m pytest tests/test_production_deviation_case_pqc.py` from this directory.
