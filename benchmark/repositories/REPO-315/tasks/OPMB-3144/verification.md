# Verification

From `benchmark/repositories/REPO-315`, run `python -m pytest tests/test_e_v_charge_session.py` and `python -m pytest tests/test_e_v_charge_session_pqc.py`. Exercise `sign_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-315/`.
