# NewsCorrectionLedger

Record signed corrections linking an article revision to corrected content digest. This synthetic cloud workflow stores immutable signed correction records in SQLite, applies application-specific claim checks, supports scoped verification and permits withdrawal.

The classical baseline uses ECDSA P-256 with SHA-256. The separate reference uses ML-DSA-65 (FIPS 204). Install `requirements.txt`; run `python -m pytest tests/test_newscorrectionledger.py -q` and `python -m pytest tests/test_newscorrectionledger_pqc.py -q` independently.

All data is fictional. The tests are not a security proof or production-readiness claim.
