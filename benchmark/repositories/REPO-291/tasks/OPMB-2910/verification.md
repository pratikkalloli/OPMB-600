# Verification

From `benchmark/repositories/REPO-291`, run `python -m pytest tests/test_device_trust_renewal.py` and `python -m pytest tests/test_device_trust_renewal_pqc.py`. Exercise `transition_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-291/`.
