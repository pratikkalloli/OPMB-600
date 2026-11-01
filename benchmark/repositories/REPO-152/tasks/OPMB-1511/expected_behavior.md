# Expected behavior

- Preserve the DiplomaVerify workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/diploma_verify/workflow.py, src/diploma_verify/crypto.py; the original test is `tests/test_diploma_verify.py::test_task_1511_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_diploma_verify_pqc.py::test_task_1511_identity_separates_signing_and_transport_keys`.
