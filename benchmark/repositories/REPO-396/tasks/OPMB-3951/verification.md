# Verification

From `benchmark/repositories/REPO-396`, run `python -m pytest tests/test_livestock_movement_certificate.py` and `python -m pytest tests/test_livestock_movement_certificate_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-396/`.
