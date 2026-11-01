# Verification

From `benchmark/repositories/REPO-277`, run `python -m pytest tests/test_edge_node_attestation.py` and `python -m pytest tests/test_edge_node_attestation_pqc.py`. Exercise `canonical_record`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-277/`.
