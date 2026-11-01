# Verification

From `benchmark/repositories/REPO-337`, run `python -m pytest tests/test_bus_depot_charge_dispatch.py` and `python -m pytest tests/test_bus_depot_charge_dispatch_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-337/`.
