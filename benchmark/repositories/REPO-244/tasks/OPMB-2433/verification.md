# Verification

From `benchmark/repositories/REPO-244`, run `python -m pytest tests/test_weld_procedure_release.py` and `python -m pytest tests/test_weld_procedure_release_pqc.py`. Exercise `generate_signer`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-244/`.
