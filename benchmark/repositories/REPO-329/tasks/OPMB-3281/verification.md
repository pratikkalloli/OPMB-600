# Verification

From `benchmark/repositories/REPO-329`, run `python -m pytest tests/test_inverter_protection_profile.py` and `python -m pytest tests/test_inverter_protection_profile_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-329/`.
