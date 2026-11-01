# Verification

From `benchmark/repositories/REPO-341`, run `python -m pytest tests/test_vehicle_title_transfer.py` and `python -m pytest tests/test_vehicle_title_transfer_pqc.py`. Exercise `export_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-341/`.
