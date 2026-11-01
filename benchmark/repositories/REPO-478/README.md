# ReproducibleBuildWitness

Record whether two isolated builds produced the same artifact digest. This synthetic cloud workflow stores immutable signed witness records in SQLite, applies application-specific claim checks, supports scoped verification and permits withdrawal.

The classical baseline uses ECDSA P-256 with SHA-256. The separate reference uses ML-DSA-65 (FIPS 204). Install `requirements.txt`; run `python -m pytest tests/test_reproduciblebuildwitness.py -q` and `python -m pytest tests/test_reproduciblebuildwitness_pqc.py -q` independently.

All data is fictional. The tests are not a security proof or production-readiness claim.
