# Verification

From `benchmark/repositories/REPO-377`, run `python -m pytest tests/test_base_station_clock_attestation.py` and `python -m pytest tests/test_base_station_clock_attestation_pqc.py`. Exercise `sign_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-377/`.
