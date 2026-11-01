# Verification

From `benchmark/repositories/REPO-384`, run `python -m pytest tests/test_packet_broker_filter_update.py` and `python -m pytest tests/test_packet_broker_filter_update_pqc.py`. Exercise `verify_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-384/`.
