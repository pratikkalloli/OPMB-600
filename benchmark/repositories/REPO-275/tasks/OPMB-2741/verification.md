# Verification

From `benchmark/repositories/REPO-275`, run `python -m pytest tests/test_gateway_join_approval.py` and `python -m pytest tests/test_gateway_join_approval_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-275/`.
