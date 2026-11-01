# Verification

From `benchmark/repositories/REPO-273`, run `python -m pytest tests/test_firmware_rollout_ring.py` and `python -m pytest tests/test_firmware_rollout_ring_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-273/`.
