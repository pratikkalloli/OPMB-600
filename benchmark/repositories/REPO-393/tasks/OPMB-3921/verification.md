# Verification

From `benchmark/repositories/REPO-393`, run `python -m pytest tests/test_crop_spray_permit.py` and `python -m pytest tests/test_crop_spray_permit_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-393/`.
