# Verification

From `benchmark/repositories/REPO-307`, run `python -m pytest tests/test_grid_topology_snapshot.py` and `python -m pytest tests/test_grid_topology_snapshot_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-307/`.
