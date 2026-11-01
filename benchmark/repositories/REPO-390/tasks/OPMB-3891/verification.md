# Verification

From `benchmark/repositories/REPO-390`, run `python -m pytest tests/test_telecom_data_retention_freeze.py` and `python -m pytest tests/test_telecom_data_retention_freeze_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-390/`.
