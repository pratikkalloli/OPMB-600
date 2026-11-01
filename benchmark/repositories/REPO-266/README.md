# SparePartCompatibility

Approves a replacement part against machine model, revision, and safety class before installation.

Workflow: Approves a replacement part against machine model, revision, and safety class before installation; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_spare_part_compatibility.py` and `python -m pytest tests/test_spare_part_compatibility_pqc.py` from this directory.

## Domain workflow

Original and PQC services implement `approve_spare_part_fit` for this application's documented operational rule. The decision requires signed approval and is recorded atomically with the workflow transition.
