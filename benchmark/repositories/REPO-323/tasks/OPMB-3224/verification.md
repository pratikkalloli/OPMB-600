# Verification

From `benchmark/repositories/REPO-323`, run `python -m pytest tests/test_grid_firmware_release.py` and `python -m pytest tests/test_grid_firmware_release_pqc.py`. Exercise `sign_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-323/`.
