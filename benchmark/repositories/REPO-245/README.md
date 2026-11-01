# BatchYieldCertificate

Certifies good and rejected unit counts for a completed manufacturing lot and links the totals to its shift and inspection station.

Workflow: Lot closeout, yield reconciliation, quality signoff, certificate publication, and correction through a new revision.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_batch_yield_certificate.py` and `python -m pytest tests/test_batch_yield_certificate_pqc.py` from this directory.
