# Verification

From `benchmark/repositories/REPO-348`, run `python -m pytest tests/test_ferry_passenger_manifest.py` and `python -m pytest tests/test_ferry_passenger_manifest_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-348/`.
