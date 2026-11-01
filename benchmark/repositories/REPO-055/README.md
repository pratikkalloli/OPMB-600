# DisasterRecovery

DisasterRecovery creates encrypted, signed system recovery snapshots. Restore planning selects snapshots available at a requested recovery time; restore validates the signed manifest and authenticated payload, records restore history, and supports snapshot comparison. Key rotation preserves historic key versions for older snapshots. This is a synthetic recovery simulation.

## Run the test suites

Install the pinned dependencies with `python -m pip install -r requirements.txt`. Run the classical application tests with `python -m pytest tests/test_disasterrecovery.py -q`. To run the separate PQC reference tests, set `PYTHONPATH` to `migrated_reference` and run `python -m pytest tests/test_disasterrecovery_pqc.py -q`. The reference uses ML-KEM-768, ML-DSA-65, HKDF-SHA-256, and AES-GCM where the workflow requires key establishment and protected data. All sample data is fictional.
