# CloudWebhookRegistry

Register tenant webhook endpoints with signed secret digests and versions. This synthetic cloud workflow stores immutable signed webhook records in SQLite, applies application-specific claim checks, supports scoped verification and permits withdrawal.

The classical baseline uses ECDSA P-256 with SHA-256. The separate reference uses ML-DSA-65 (FIPS 204). Install `requirements.txt`; run `python -m pytest tests/test_cloudwebhookregistry.py -q` and `python -m pytest tests/test_cloudwebhookregistry_pqc.py -q` independently.

All data is fictional. The tests are not a security proof or production-readiness claim.
