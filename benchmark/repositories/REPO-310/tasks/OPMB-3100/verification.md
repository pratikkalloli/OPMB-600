# Verification

From `benchmark/repositories/REPO-310`, run `python -m pytest tests/test_battery_dispatch_receipt.py` and `python -m pytest tests/test_battery_dispatch_receipt_pqc.py`. Exercise `transition_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-310/`.
