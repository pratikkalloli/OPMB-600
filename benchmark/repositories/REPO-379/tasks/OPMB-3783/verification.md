# Verification

From `benchmark/repositories/REPO-379`, run `python -m pytest tests/test_roaming_partner_profile.py` and `python -m pytest tests/test_roaming_partner_profile_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-379/`.
