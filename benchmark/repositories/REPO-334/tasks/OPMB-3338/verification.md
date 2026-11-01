# Verification

From `benchmark/repositories/REPO-334`, run `python -m pytest tests/test_port_container_seal.py` and `python -m pytest tests/test_port_container_seal_pqc.py`. Exercise `seal_artifact`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-334/`.
