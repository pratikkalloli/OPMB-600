# Expected behavior

- Preserve the CustomsDeclaration workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/customs_declaration/workflow.py, src/customs_declaration/crypto.py; the original test is `tests/test_customs_declaration.py::test_task_2279_rotation_retires_old_key_version` and PQC migration test is `tests/test_customs_declaration_pqc.py::test_task_2279_rotation_retires_old_key_version`.
