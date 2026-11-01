# EncryptedNotebook

EncryptedNotebook stores versioned synthetic notes for notebook owners. Note content is encrypted to owner key versions, and every immutable version carries a signed content digest. Owners can verify history and restore prior versions. Key rotation adds a new recipient key version while retaining old key versions for historical decryption.

## Run the test suites

Install the pinned dependencies with `python -m pip install -r requirements.txt`. Run the classical application tests with `python -m pytest tests/test_encryptednotebook.py -q`. To run the separate PQC reference tests, set `PYTHONPATH` to `migrated_reference` and run `python -m pytest tests/test_encryptednotebook_pqc.py -q`. The reference uses ML-KEM-768, ML-DSA-65, HKDF-SHA-256, and AES-GCM where the workflow requires key establishment and protected data. All sample data is fictional.
