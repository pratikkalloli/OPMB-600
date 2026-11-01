# EnergyMeter

EnergyMeter simulates utility meters submitting signed consumption readings. Records bind meter ID, sequence, timestamp, reading value, and unit. The service validates sequence and time, detects tampering, supports signing-key rotation, and exposes an audit history. No real utility data is present.

## Run the test suites

Install the pinned dependencies with `python -m pip install -r requirements.txt`. Run the classical application tests with `python -m pytest tests/test_energymeter.py -q`. To run the separate PQC reference tests, set `PYTHONPATH` to `migrated_reference` and run `python -m pytest tests/test_energymeter_pqc.py -q`. The reference uses ML-KEM-768, ML-DSA-65, HKDF-SHA-256, and AES-GCM where the workflow requires key establishment and protected data. All sample data is fictional.
