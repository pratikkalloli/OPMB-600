# Verification

From `benchmark/repositories/REPO-283`, run `python -m pytest tests/test_remote_probe_registry.py` and `python -m pytest tests/test_remote_probe_registry_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-283/`.
