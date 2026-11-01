# Verification

From `benchmark/repositories/REPO-399`, run `python -m pytest tests/test_weather_station_calibration.py` and `python -m pytest tests/test_weather_station_calibration_pqc.py`. Exercise `verify_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-399/`.
