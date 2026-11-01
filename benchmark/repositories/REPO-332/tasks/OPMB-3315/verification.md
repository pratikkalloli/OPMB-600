# Verification

From `benchmark/repositories/REPO-332`, run `python -m pytest tests/test_cold_chain_transfer.py` and `python -m pytest tests/test_cold_chain_transfer_pqc.py`. Exercise `verify_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-332/`.
