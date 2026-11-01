# Verification

From `benchmark/repositories/REPO-267`, run `python -m pytest tests/test_clean_in_place_record.py` and `python -m pytest tests/test_clean_in_place_record_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-267/`.
