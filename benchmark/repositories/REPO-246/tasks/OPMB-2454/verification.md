# Verification

From `benchmark/repositories/REPO-246`, run `python -m pytest tests/test_tool_change_authorization.py` and `python -m pytest tests/test_tool_change_authorization_pqc.py`. Exercise `sign_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-246/`.
