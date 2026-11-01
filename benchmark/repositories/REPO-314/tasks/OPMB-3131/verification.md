# Verification

From `benchmark/repositories/REPO-314`, run `python -m pytest tests/test_carbon_intensity_attestation.py` and `python -m pytest tests/test_carbon_intensity_attestation_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-314/`.
