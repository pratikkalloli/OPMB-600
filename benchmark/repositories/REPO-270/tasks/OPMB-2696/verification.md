# Verification

From `benchmark/repositories/REPO-270`, run `python -m pytest tests/test_production_sample_custody.py` and `python -m pytest tests/test_production_sample_custody_pqc.py`. Exercise `export_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-270/`.
