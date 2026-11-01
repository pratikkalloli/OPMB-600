# CredentialRevocation

CredentialRevocation records synthetic credential revocations and publishes signed verifier feeds. Feed sequence and issue/expiry times are checked to reject stale or rolled-back updates. Publisher signing keys can rotate while historic public keys remain available to verify old feeds.

## Run the test suites

Install the pinned dependencies with `python -m pip install -r requirements.txt`. Run the classical application tests with `python -m pytest tests/test_credentialrevocation.py -q`. To run the separate PQC reference tests, set `PYTHONPATH` to `migrated_reference` and run `python -m pytest tests/test_credentialrevocation_pqc.py -q`. The reference uses ML-KEM-768, ML-DSA-65, HKDF-SHA-256, and AES-GCM where the workflow requires key establishment and protected data. All sample data is fictional.
