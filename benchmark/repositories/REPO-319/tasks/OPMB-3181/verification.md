# Verification

From `benchmark/repositories/REPO-319`, run `python -m pytest tests/test_outage_restoration_log.py` and `python -m pytest tests/test_outage_restoration_log_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-319/`.
