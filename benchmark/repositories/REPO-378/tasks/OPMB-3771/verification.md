# Verification

From `benchmark/repositories/REPO-378`, run `python -m pytest tests/test_qo_s_contract_revision.py` and `python -m pytest tests/test_qo_s_contract_revision_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-378/`.
