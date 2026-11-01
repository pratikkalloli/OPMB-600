# SpectrumGrantLedger

Records synthetic spectrum grant intervals, geography, and renewal decisions.

Workflow: Records synthetic spectrum grant intervals, geography, and renewal decisions; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_spectrum_grant_ledger.py` and `python -m pytest tests/test_spectrum_grant_ledger_pqc.py` from this directory.
