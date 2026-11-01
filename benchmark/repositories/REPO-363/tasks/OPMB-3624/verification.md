# Verification

From `benchmark/repositories/REPO-363`, run `python -m pytest tests/test_peering_key_agreement.py` and `python -m pytest tests/test_peering_key_agreement_pqc.py`. Exercise `sign_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-363/`.
