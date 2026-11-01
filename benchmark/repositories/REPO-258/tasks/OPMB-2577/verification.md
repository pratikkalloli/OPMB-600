# Verification

From `benchmark/repositories/REPO-258`, run `python -m pytest tests/test_production_scrap_voucher.py` and `python -m pytest tests/test_production_scrap_voucher_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-258/`.
