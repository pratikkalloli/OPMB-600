# Verification

From `benchmark/repositories/REPO-338`, run `python -m pytest tests/test_maritime_bill_of_lading.py` and `python -m pytest tests/test_maritime_bill_of_lading_pqc.py`. Exercise `verify_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-338/`.
