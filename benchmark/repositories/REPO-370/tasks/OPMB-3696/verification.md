# Verification

From `benchmark/repositories/REPO-370`, run `python -m pytest tests/test_spectrum_grant_ledger.py` and `python -m pytest tests/test_spectrum_grant_ledger_pqc.py`. Exercise `export_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-370/`.
