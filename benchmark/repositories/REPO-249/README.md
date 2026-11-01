# MachineInterlockPermit

Issues epoch-bound machine interlock permits after a safety case is reviewed and blocks restart on stale or superseded interlock settings.

Workflow: Safety-case review, interlock epoch issuance, operator acknowledgment, and restart authorization.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_machine_interlock_permit.py` and `python -m pytest tests/test_machine_interlock_permit_pqc.py` from this directory.
