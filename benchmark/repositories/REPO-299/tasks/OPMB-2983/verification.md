# Verification

From `benchmark/repositories/REPO-299`, run `python -m pytest tests/test_low_power_network_join.py` and `python -m pytest tests/test_low_power_network_join_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-299/`.
