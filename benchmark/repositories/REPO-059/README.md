# InventoryHandoff

InventoryHandoff tracks synthetic items and batches across sender/recipient transfers. Each transfer record binds item, batch, sequence, timestamp, sender, and recipient; each actor signs the record. Verification checks custody continuity and detects altered or missing entries.

## Run the test suites

Install the pinned dependencies with `python -m pip install -r requirements.txt`. Run the classical application tests with `python -m pytest tests/test_inventoryhandoff.py -q`. To run the separate PQC reference tests, set `PYTHONPATH` to `migrated_reference` and run `python -m pytest tests/test_inventoryhandoff_pqc.py -q`. The reference uses ML-KEM-768, ML-DSA-65, HKDF-SHA-256, and AES-GCM where the workflow requires key establishment and protected data. All sample data is fictional.
