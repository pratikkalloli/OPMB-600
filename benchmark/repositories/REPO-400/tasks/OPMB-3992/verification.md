# Verification

From `benchmark/repositories/REPO-400`, run `python -m pytest tests/test_beehive_health_observation.py` and `python -m pytest tests/test_beehive_health_observation_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-400/`.
