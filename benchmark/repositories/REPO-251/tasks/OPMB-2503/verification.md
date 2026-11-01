# Verification

From `benchmark/repositories/REPO-251`, run `python -m pytest tests/test_serialized_machine_passport.py` and `python -m pytest tests/test_serialized_machine_passport_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-251/`.
