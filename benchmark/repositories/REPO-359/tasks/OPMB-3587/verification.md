# Verification

From `benchmark/repositories/REPO-359`, run `python -m pytest tests/test_train_consist_revision.py` and `python -m pytest tests/test_train_consist_revision_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-359/`.
