# Verification

From `benchmark/repositories/REPO-357`, run `python -m pytest tests/test_container_weight_ticket.py` and `python -m pytest tests/test_container_weight_ticket_pqc.py`. Exercise `seal_artifact`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-357/`.
