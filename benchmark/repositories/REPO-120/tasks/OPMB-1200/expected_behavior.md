# Expected behavior

- Preserve the DeviceMaintenanceLog workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/device_maintenance_log/workflow.py, src/device_maintenance_log/crypto.py; the original test is `tests/test_device_maintenance_log.py::test_task_1200_revocation_ledger_persistence_and_cli_workflow` and PQC migration test is `tests/test_device_maintenance_log_pqc.py::test_task_1200_revocation_ledger_persistence_and_cli_workflow`.
