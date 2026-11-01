# Verification

From `benchmark/repositories/REPO-373`, run `python -m pytest tests/test_network_change_window.py` and `python -m pytest tests/test_network_change_window_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-373/`.
