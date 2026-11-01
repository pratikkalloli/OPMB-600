# Verification

From `benchmark/repositories/REPO-279`, run `python -m pytest tests/test_telemetry_frame_seal.py` and `python -m pytest tests/test_telemetry_frame_seal_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-279/`.
