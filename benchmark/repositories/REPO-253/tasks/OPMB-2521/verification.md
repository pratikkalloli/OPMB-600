# Verification

From `benchmark/repositories/REPO-253`, run `python -m pytest tests/test_tool_wear_forecast_case.py` and `python -m pytest tests/test_tool_wear_forecast_case_pqc.py`. Exercise `validate_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-253/`.
