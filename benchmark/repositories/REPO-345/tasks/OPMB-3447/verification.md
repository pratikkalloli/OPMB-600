# Verification

From `benchmark/repositories/REPO-345`, run `python -m pytest tests/test_customs_inspection_packet.py` and `python -m pytest tests/test_customs_inspection_packet_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-345/`.
