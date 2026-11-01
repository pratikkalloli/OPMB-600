# Verification

From `benchmark/repositories/REPO-248`, run `python -m pytest tests/test_production_deviation_case.py` and `python -m pytest tests/test_production_deviation_case_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-248/`.
