# Expected behavior

- Preserve the AdmissionOffer workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/admission_offer/workflow.py, src/admission_offer/crypto.py; the original test is `tests/test_admission_offer.py::test_task_1532_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_admission_offer_pqc.py::test_task_1532_public_key_encoding_round_trips_and_binds_purpose`.
