# Expected behavior

- Preserve the EnrollmentProof workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/enrollment_proof/workflow.py, src/enrollment_proof/crypto.py; the original test is `tests/test_enrollment_proof.py::test_task_1705_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_enrollment_proof_pqc.py::test_task_1705_canonical_record_encoding_is_stable`.
