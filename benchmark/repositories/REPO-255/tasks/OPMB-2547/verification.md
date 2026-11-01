# Verification

From `benchmark/repositories/REPO-255`, run `python -m pytest tests/test_packaging_artwork_release.py` and `python -m pytest tests/test_packaging_artwork_release_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-255/`.
