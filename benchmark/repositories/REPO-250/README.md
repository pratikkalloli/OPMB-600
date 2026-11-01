# ComponentTraceLot

Links a received component lot to its source material digest and production batch so downstream assemblies can verify provenance before use.

Workflow: Receiving inspection, source-lot binding, production consumption, and traceability export.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_component_trace_lot.py` and `python -m pytest tests/test_component_trace_lot_pqc.py` from this directory.
