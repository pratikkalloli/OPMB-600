# Verification

From `benchmark/repositories/REPO-382`, run `python -m pytest tests/test_emergency_broadcast_authorization.py` and `python -m pytest tests/test_emergency_broadcast_authorization_pqc.py`. Exercise `export_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-382/`.
