# Expected behavior

- Preserve the ClinicalAlertAck workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/clinical_alert_ack/workflow.py, src/clinical_alert_ack/crypto.py; the original test is `tests/test_clinical_alert_ack.py::test_task_1060_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_clinical_alert_ack_pqc.py::test_task_1060_revocation_ledger_persistence_and_cli_workflow`.
