# Verification

From `benchmark/repositories/REPO-342`, run `python -m pytest tests/test_taxi_shift_settlement.py` and `python -m pytest tests/test_taxi_shift_settlement_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-342/`.
