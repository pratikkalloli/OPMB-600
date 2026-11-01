# Expected behavior

- Preserve the FacultyCredential workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/faculty_credential/workflow.py, src/faculty_credential/crypto.py; the original test is `tests/test_faculty_credential.py::test_task_1692_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_faculty_credential_pqc.py::test_task_1692_public_key_encoding_round_trips_and_binds_purpose`.
