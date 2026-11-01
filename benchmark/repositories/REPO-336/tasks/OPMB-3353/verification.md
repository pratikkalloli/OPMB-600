# Verification

From `benchmark/repositories/REPO-336`, run `python -m pytest tests/test_fleet_route_exception.py` and `python -m pytest tests/test_fleet_route_exception_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-336/`.
