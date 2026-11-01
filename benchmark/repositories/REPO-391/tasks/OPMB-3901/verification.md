# Verification

From `benchmark/repositories/REPO-391`, run `python -m pytest tests/test_irrigation_zone_schedule.py` and `python -m pytest tests/test_irrigation_zone_schedule_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-391/`.
