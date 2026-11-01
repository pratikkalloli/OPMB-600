# Verification

From `benchmark/repositories/REPO-292`, run `python -m pytest tests/test_microcontroller_build_proof.py` and `python -m pytest tests/test_microcontroller_build_proof_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-292/`.
