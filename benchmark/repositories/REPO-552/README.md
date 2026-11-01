# AvailabilityBlockSeal

Publish a user availability window with visibility and calendar scope. This synthetic cloud workflow stores immutable signed availability_block records in SQLite, applies application-specific claim checks, supports scoped verification and permits withdrawal.

The classical baseline uses ECDSA P-256 with SHA-256. The separate reference uses ML-DSA-65 (FIPS 204). Install `requirements.txt`; run `python -m pytest tests/test_availabilityblockseal.py -q` and `python -m pytest tests/test_availabilityblockseal_pqc.py -q` independently.

All data is fictional. The tests are not a security proof or production-readiness claim.
