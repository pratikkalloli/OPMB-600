# Verification

From `benchmark/repositories/REPO-266`, run `python -m pytest tests/test_spare_part_compatibility.py` and `python -m pytest tests/test_spare_part_compatibility_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-266/`.
