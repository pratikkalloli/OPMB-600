# FeatureSchemaApproval

Approve a feature-store schema digest under reviewer decision and store identity. This synthetic cloud workflow stores immutable signed approval records in SQLite, applies application-specific claim checks, supports scoped verification and permits withdrawal.

The classical baseline uses ECDSA P-256 with SHA-256. The separate reference uses ML-DSA-65 (FIPS 204). Install `requirements.txt`; run `python -m pytest tests/test_featureschemaapproval.py -q` and `python -m pytest tests/test_featureschemaapproval_pqc.py -q` independently.

All data is fictional. The tests are not a security proof or production-readiness claim.
