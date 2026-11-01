# StorageTenantHandoff

Transfer storage ownership between tenants with a manifest digest. This synthetic cloud workflow stores immutable signed tenant handoff records in SQLite, applies application-specific claim checks, supports scoped verification and permits withdrawal.

The classical baseline uses ECDSA P-256 with SHA-256. The separate reference uses ML-DSA-65 (FIPS 204). Install `requirements.txt`; run `python -m pytest tests/test_storagetenanthandoff.py -q` and `python -m pytest tests/test_storagetenanthandoff_pqc.py -q` independently.

All data is fictional. The tests are not a security proof or production-readiness claim.
