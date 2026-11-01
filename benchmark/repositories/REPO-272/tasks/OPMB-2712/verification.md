# Verification

From `benchmark/repositories/REPO-272`, run `python -m pytest tests/test_sensor_calibration_chain.py` and `python -m pytest tests/test_sensor_calibration_chain_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-272/`.
