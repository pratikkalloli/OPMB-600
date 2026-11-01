# Verification

From `benchmark/repositories/REPO-380`, run `python -m pytest tests/test_synthetic_intercept_audit.py` and `python -m pytest tests/test_synthetic_intercept_audit_pqc.py`. Exercise `sign_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-380/`.
