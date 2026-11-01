# Verification

From `benchmark/repositories/REPO-296`, run `python -m pytest tests/test_fleet_certificate_rotation.py` and `python -m pytest tests/test_fleet_certificate_rotation_pqc.py`. Exercise `seal_artifact`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-296/`.
