# Verification

From `benchmark/repositories/REPO-274`, run `python -m pytest tests/test_drone_fleet_command.py` and `python -m pytest tests/test_drone_fleet_command_pqc.py`. Exercise `seal_artifact`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-274/`.
