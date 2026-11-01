# EdgeFunctionRelease

Publish signed edge-function releases with artifact digest and rollout channel. This synthetic cloud workflow stores immutable signed release records in SQLite, applies application-specific claim checks, supports scoped verification and permits withdrawal.

The classical baseline uses ECDSA P-256 with SHA-256. The separate reference uses ML-DSA-65 (FIPS 204). Install `requirements.txt`; run `python -m pytest tests/test_edgefunctionrelease.py -q` and `python -m pytest tests/test_edgefunctionrelease_pqc.py -q` independently.

All data is fictional. The tests are not a security proof or production-readiness claim.
