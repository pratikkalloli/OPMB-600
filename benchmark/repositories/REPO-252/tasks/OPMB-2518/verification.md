# Verification

From `benchmark/repositories/REPO-252`, run `python -m pytest tests/test_torque_audit_ledger.py` and `python -m pytest tests/test_torque_audit_ledger_pqc.py`. Exercise `seal_artifact`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-252/`.
