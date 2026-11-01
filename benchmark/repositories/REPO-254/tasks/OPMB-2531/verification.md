# Verification

From `benchmark/repositories/REPO-254`, run `python -m pytest tests/test_furnace_cycle_witness.py` and `python -m pytest tests/test_furnace_cycle_witness_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-254/`.
