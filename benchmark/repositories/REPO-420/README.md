# FarmProducePackingLot

Links harvested produce to packing line, grade result, and shipping destination.

Workflow: Links harvested produce to packing line, grade result, and shipping destination; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_farm_produce_packing_lot.py` and `python -m pytest tests/test_farm_produce_packing_lot_pqc.py` from this directory.
