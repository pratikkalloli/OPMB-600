# Verification

From `benchmark/repositories/REPO-372`, run `python -m pytest tests/test_service_chain_activation.py` and `python -m pytest tests/test_service_chain_activation_pqc.py`. Exercise `export_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-372/`.
