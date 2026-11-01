# Verification

From `benchmark/repositories/REPO-353`, run `python -m pytest tests/test_shipping_hazard_declaration.py` and `python -m pytest tests/test_shipping_hazard_declaration_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-353/`.
