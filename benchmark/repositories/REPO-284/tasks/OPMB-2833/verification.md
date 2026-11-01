# Verification

From `benchmark/repositories/REPO-284`, run `python -m pytest tests/test_device_recovery_ticket.py` and `python -m pytest tests/test_device_recovery_ticket_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-284/`.
