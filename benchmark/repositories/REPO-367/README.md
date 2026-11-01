# EdgeCacheInvalidate

Issues scoped cache invalidation instructions and records acknowledgements from edge nodes.

Workflow: Issues scoped cache invalidation instructions and records acknowledgements from edge nodes; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_edge_cache_invalidate.py` and `python -m pytest tests/test_edge_cache_invalidate_pqc.py` from this directory.
