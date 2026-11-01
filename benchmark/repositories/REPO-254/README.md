# FurnaceCycleWitness

Binds furnace temperature-time evidence to a heat-treatment batch and blocks release when the cycle window is violated.

Workflow: Binds furnace temperature-time evidence to a heat-treatment batch and blocks release when the cycle window is violated; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_furnace_cycle_witness.py` and `python -m pytest tests/test_furnace_cycle_witness_pqc.py` from this directory.

## Domain workflow

Both the original and PQC services implement `witness_furnace_soak_window`. It enforces the application's stated business rule and records the decision with the signed record's workflow event.
