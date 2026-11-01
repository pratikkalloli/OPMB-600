# Expected behavior

- Preserve the ReimbursementEvidence workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/reimbursement_evidence/workflow.py, src/reimbursement_evidence/crypto.py; the original test is `tests/test_reimbursement_evidence.py::test_task_1083_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_reimbursement_evidence_pqc.py::test_task_1083_malformed_serialization_and_wrong_purpose_are_rejected`.
