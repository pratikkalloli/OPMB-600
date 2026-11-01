# DataMarketplace

DataMarketplace registers fictional data providers and versioned assets. Each published asset has a signed manifest containing the provider, dataset version, metadata digest, and content digest. Asset exchange encrypts the data to a consumer, verifies the provider signature on retrieval, and records an access audit.

## Run the test suites

Install the pinned dependencies with `python -m pip install -r requirements.txt`. Run the classical application tests with `python -m pytest tests/test_datamarketplace.py -q`. To run the separate PQC reference tests, set `PYTHONPATH` to `migrated_reference` and run `python -m pytest tests/test_datamarketplace_pqc.py -q`. The reference uses ML-KEM-768, ML-DSA-65, HKDF-SHA-256, and AES-GCM where the workflow requires key establishment and protected data. All sample data is fictional.
