# ProductionScrapVoucher

Authorizes scrapping a quantity of serialized work in process and preserves the quality disposition.

Workflow: Authorizes scrapping a quantity of serialized work in process and preserves the quality disposition; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_production_scrap_voucher.py` and `python -m pytest tests/test_production_scrap_voucher_pqc.py` from this directory.
