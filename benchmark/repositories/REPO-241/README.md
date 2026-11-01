# WorkcellRecipeVault

Controls revisioned production recipes by workcell and approver, preventing an unreviewed recipe from being issued to a line.

Workflow: Recipe authoring, quality review, controlled release, and retirement for one manufacturing workcell.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_workcell_recipe_vault.py` and `python -m pytest tests/test_workcell_recipe_vault_pqc.py` from this directory.

## Domain workflow

The original and PQC service layers expose `release_recipe`. This operation verifies the current signed record, enforces the application's business-specific policy, and records the resulting decision and evidence transactionally.
