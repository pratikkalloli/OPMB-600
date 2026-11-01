# Verification

From `benchmark/repositories/REPO-317`, run `python -m pytest tests/test_fuel_blend_certificate.py` and `python -m pytest tests/test_fuel_blend_certificate_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-317/`.
