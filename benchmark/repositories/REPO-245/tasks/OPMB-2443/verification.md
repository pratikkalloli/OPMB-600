# Verification

From `benchmark/repositories/REPO-245`, run `python -m pytest tests/test_batch_yield_certificate.py` and `python -m pytest tests/test_batch_yield_certificate_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-245/`.
