# Verification

From `benchmark/repositories/REPO-242`, run `python -m pytest tests/test_line_clearance_token.py` and `python -m pytest tests/test_line_clearance_token_pqc.py`. Exercise `sign_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-242/`.
