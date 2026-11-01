# TrainConsistRevision

Versions train consist order and checks vehicle compatibility before departure.

Workflow: Versions train consist order and checks vehicle compatibility before departure; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_train_consist_revision.py` and `python -m pytest tests/test_train_consist_revision_pqc.py` from this directory.
