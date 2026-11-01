# Expected behavior

- Preserve the MaterialTransfer workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/material_transfer/workflow.py, src/material_transfer/crypto.py; the original test is `tests/test_material_transfer.py::test_task_1657_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_material_transfer_pqc.py::test_task_1657_signature_rejects_tamper_wrong_key_and_downgrade`.
