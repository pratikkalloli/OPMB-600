# Expected behavior

- Preserve the PrescriptionDispense workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/prescription_dispense/workflow.py, src/prescription_dispense/crypto.py; the original test is `tests/test_prescription_dispense.py::test_task_0926_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_prescription_dispense_pqc.py::test_task_0926_signature_binds_record_context_and_validity`.
