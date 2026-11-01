# Verification

From `benchmark/repositories/REPO-394`, run `python -m pytest tests/test_seed_lot_provenance.py` and `python -m pytest tests/test_seed_lot_provenance_pqc.py`. Exercise `sign_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-394/`.
