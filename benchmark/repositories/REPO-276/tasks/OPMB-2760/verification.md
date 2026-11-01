# Verification

From `benchmark/repositories/REPO-276`, run `python -m pytest tests/test_device_ownership_transfer.py` and `python -m pytest tests/test_device_ownership_transfer_pqc.py`. Exercise `transition_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-276/`.
