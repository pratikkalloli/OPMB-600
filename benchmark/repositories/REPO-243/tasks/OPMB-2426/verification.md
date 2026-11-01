# Verification

From `benchmark/repositories/REPO-243`, run `python -m pytest tests/test_fixture_calibration_dossier.py` and `python -m pytest tests/test_fixture_calibration_dossier_pqc.py`. Exercise `export_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-243/`.
