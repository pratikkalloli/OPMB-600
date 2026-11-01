# MusicSessionSplitSheet

Record contributor shares for a music session under a signed split sheet. This synthetic cloud workflow stores immutable signed split_sheet records in SQLite, applies application-specific claim checks, supports scoped verification and permits withdrawal.

The classical baseline uses ECDSA P-256 with SHA-256. The separate reference uses ML-DSA-65 (FIPS 204). Install `requirements.txt`; run `python -m pytest tests/test_musicsessionsplitsheet.py -q` and `python -m pytest tests/test_musicsessionsplitsheet_pqc.py -q` independently.

All data is fictional. The tests are not a security proof or production-readiness claim.
