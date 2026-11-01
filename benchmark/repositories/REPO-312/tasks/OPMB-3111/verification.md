# Verification

From `benchmark/repositories/REPO-312`, run `python -m pytest tests/test_hydro_reservoir_release.py` and `python -m pytest tests/test_hydro_reservoir_release_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-312/`.
