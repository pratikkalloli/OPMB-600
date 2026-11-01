# Verification

From `benchmark/repositories/REPO-369`, run `python -m pytest tests/test_tower_access_permit.py` and `python -m pytest tests/test_tower_access_permit_pqc.py`. Exercise `sign_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-369/`.
