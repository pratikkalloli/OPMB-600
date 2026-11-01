# Verification

From `benchmark/repositories/REPO-383`, run `python -m pytest tests/test_network_telemetry_checkpoint.py` and `python -m pytest tests/test_network_telemetry_checkpoint_pqc.py`. Exercise `seal_artifact`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-383/`.
