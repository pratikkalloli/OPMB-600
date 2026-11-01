# ConsumableShelfLifeCard

Tracks lot expiry and opened-container life for process consumables used by a production cell.

Workflow: Tracks lot expiry and opened-container life for process consumables used by a production cell; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_consumable_shelf_life_card.py` and `python -m pytest tests/test_consumable_shelf_life_card_pqc.py` from this directory.

## Domain workflow

Original and PQC services implement `release_process_consumable` for this application's documented operational rule. The decision requires signed approval and is recorded atomically with the workflow transition.
