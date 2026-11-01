# Verification

From `benchmark/repositories/REPO-293`, run `python -m pytest tests/test_camera_privacy_zone.py` and `python -m pytest tests/test_camera_privacy_zone_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-293/`.
