# Verification

From `benchmark/repositories/REPO-352`, run `python -m pytest tests/test_autonomous_convoy_join.py` and `python -m pytest tests/test_autonomous_convoy_join_pqc.py`. Exercise `export_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-352/`.
