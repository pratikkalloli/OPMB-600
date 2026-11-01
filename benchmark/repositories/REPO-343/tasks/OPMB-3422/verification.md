# Verification

From `benchmark/repositories/REPO-343`, run `python -m pytest tests/test_aircraft_ground_power_log.py` and `python -m pytest tests/test_aircraft_ground_power_log_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-343/`.
