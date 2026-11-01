# Verification

From `benchmark/repositories/REPO-403`, run `python -m pytest tests/test_harvest_bin_handoff.py` and `python -m pytest tests/test_harvest_bin_handoff_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-403/`.
