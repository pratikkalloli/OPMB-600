# Verification

From `benchmark/repositories/REPO-281`, run `python -m pytest tests/test_smart_lock_lease.py` and `python -m pytest tests/test_smart_lock_lease_pqc.py`. Exercise `transition_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-281/`.
