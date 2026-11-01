# TenderProof

TenderProof models fictional procurement tenders with bidder registration, signed bid records, submission deadlines, and confidential bid-package encryption to an evaluator. Evaluator access checks the bidder signature before decrypting and records an audit entry. This is a synthetic procurement workflow.

## Run the test suites

Install the pinned dependencies with `python -m pip install -r requirements.txt`. Run the classical application tests with `python -m pytest tests/test_tenderproof.py -q`. To run the separate PQC reference tests, set `PYTHONPATH` to `migrated_reference` and run `python -m pytest tests/test_tenderproof_pqc.py -q`. The reference uses ML-KEM-768, ML-DSA-65, HKDF-SHA-256, and AES-GCM where the workflow requires key establishment and protected data. All sample data is fictional.
