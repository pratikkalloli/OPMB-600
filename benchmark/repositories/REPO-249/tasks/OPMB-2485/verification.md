# Verification

From `benchmark/repositories/REPO-249`, run `python -m pytest tests/test_machine_interlock_permit.py` and `python -m pytest tests/test_machine_interlock_permit_pqc.py`. Exercise `verify_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-249/`.
