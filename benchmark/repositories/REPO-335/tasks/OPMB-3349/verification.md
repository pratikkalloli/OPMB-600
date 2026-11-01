# Verification

From `benchmark/repositories/REPO-335`, run `python -m pytest tests/test_transit_operator_credential.py` and `python -m pytest tests/test_transit_operator_credential_pqc.py`. Exercise `open_artifact`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-335/`.
