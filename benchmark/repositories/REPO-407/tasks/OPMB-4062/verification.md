# Verification

From `benchmark/repositories/REPO-407`, run `python -m pytest tests/test_river_gauge_observation.py` and `python -m pytest tests/test_river_gauge_observation_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-407/`.
