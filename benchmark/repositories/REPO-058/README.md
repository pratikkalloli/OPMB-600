# RemoteAttestation

RemoteAttestation is a software simulation for workload measurements. It registers fictional workloads, creates time-bounded signed evidence packages, verifies evidence against a policy allowlist, and records verifier history. The package may be encrypted to a verifier during exchange. This simulation does not provide hardware-rooted attestation or trusted hardware support.

## Run the test suites

Install the pinned dependencies with `python -m pip install -r requirements.txt`. Run the classical application tests with `python -m pytest tests/test_remoteattestation.py -q`. To run the separate PQC reference tests, set `PYTHONPATH` to `migrated_reference` and run `python -m pytest tests/test_remoteattestation_pqc.py -q`. The reference uses ML-KEM-768, ML-DSA-65, HKDF-SHA-256, and AES-GCM where the workflow requires key establishment and protected data. All sample data is fictional.
