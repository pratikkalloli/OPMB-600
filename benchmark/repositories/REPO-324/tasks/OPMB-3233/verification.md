# Verification

From `benchmark/repositories/REPO-324`, run `python -m pytest tests/test_customer_meter_exchange.py` and `python -m pytest tests/test_customer_meter_exchange_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-324/`.
