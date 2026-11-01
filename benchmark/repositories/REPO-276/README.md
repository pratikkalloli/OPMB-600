# DeviceOwnershipTransfer

Transfers a device between fictional owners while revoking the prior owner's access grant.

Workflow: Transfers a device between fictional owners while revoking the prior owner's access grant; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_device_ownership_transfer.py` and `python -m pytest tests/test_device_ownership_transfer_pqc.py` from this directory.
