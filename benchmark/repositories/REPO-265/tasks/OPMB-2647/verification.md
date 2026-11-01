# Verification

From `benchmark/repositories/REPO-265`, run `python -m pytest tests/test_quality_hold_release.py` and `python -m pytest tests/test_quality_hold_release_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-265/`.
