# Verification

From `benchmark/repositories/REPO-362`, run `python -m pytest tests/test_routing_policy_bundle.py` and `python -m pytest tests/test_routing_policy_bundle_pqc.py`. Exercise `export_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-362/`.
