# Verification

From `benchmark/repositories/REPO-388`, run `python -m pytest tests/test_internet_exchange_membership.py` and `python -m pytest tests/test_internet_exchange_membership_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-388/`.
