# Verification

From `benchmark/repositories/REPO-271`, run `python -m pytest tests/test_robot_cell_enrollment.py` and `python -m pytest tests/test_robot_cell_enrollment_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-271/`.
