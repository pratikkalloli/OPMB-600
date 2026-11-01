# Expected behavior

- Preserve the ClinicalAlertAck workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/clinical_alert_ack/workflow.py, src/clinical_alert_ack/crypto.py; the original test is `tests/test_clinical_alert_ack.py::test_task_1052_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_clinical_alert_ack_pqc.py::test_task_1052_public_key_encoding_round_trips_and_binds_purpose`.
