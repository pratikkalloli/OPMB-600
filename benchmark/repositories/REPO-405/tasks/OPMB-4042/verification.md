# Verification

From `benchmark/repositories/REPO-405`, run `python -m pytest tests/test_cold_room_temperature_record.py` and `python -m pytest tests/test_cold_room_temperature_record_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-405/`.
