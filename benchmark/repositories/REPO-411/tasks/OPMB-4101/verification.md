# Verification

From `benchmark/repositories/REPO-411`, run `python -m pytest tests/test_compost_batch_maturity.py` and `python -m pytest tests/test_compost_batch_maturity_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-411/`.
