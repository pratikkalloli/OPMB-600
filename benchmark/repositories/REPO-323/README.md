# GridFirmwareRelease

Gates a simulated grid controller firmware release on compatibility and rollback evidence.

Workflow: Gates a simulated grid controller firmware release on compatibility and rollback evidence; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_grid_firmware_release.py` and `python -m pytest tests/test_grid_firmware_release_pqc.py` from this directory.
