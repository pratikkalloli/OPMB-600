# Verification

From `benchmark/repositories/REPO-241`, run `python -m pytest tests/test_workcell_recipe_vault.py` and `python -m pytest tests/test_workcell_recipe_vault_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-241/`.
