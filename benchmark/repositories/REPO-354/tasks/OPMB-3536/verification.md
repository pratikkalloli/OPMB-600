# Verification

From `benchmark/repositories/REPO-354`, run `python -m pytest tests/test_airport_baggage_custody.py` and `python -m pytest tests/test_airport_baggage_custody_pqc.py`. Exercise `export_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-354/`.
