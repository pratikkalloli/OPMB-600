# Verification

From `benchmark/repositories/REPO-289`, run `python -m pytest tests/test_sensor_batch_provenance.py` and `python -m pytest tests/test_sensor_batch_provenance_pqc.py`. Exercise `open_artifact`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-289/`.
