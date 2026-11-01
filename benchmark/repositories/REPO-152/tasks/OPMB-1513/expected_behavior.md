# Expected behavior

- Preserve the DiplomaVerify workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/diploma_verify/workflow.py, src/diploma_verify/crypto.py; the original test is `tests/test_diploma_verify.py::test_task_1513_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_diploma_verify_pqc.py::test_task_1513_malformed_serialization_and_wrong_purpose_are_rejected`.
