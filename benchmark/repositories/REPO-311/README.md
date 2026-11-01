# UtilityCrewPermit

Issues a work-zone permit for a utility crew and records clearance before re-energization.

Workflow: Issues a work-zone permit for a utility crew and records clearance before re-energization; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_utility_crew_permit.py` and `python -m pytest tests/test_utility_crew_permit_pqc.py` from this directory.
