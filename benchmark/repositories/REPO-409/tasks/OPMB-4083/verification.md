# Verification

From `benchmark/repositories/REPO-409`, run `python -m pytest tests/test_fertilizer_blend_ticket.py` and `python -m pytest tests/test_fertilizer_blend_ticket_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-409/`.
