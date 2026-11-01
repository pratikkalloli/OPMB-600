# Verification

From `benchmark/repositories/REPO-250`, run `python -m pytest tests/test_component_trace_lot.py` and `python -m pytest tests/test_component_trace_lot_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-250/`.
