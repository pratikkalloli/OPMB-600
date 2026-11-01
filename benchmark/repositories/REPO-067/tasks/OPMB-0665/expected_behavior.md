# Expected behavior

- Preserve the LoanDisclosure workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/loan_disclosure/workflow.py, src/loan_disclosure/crypto.py; the original test is `tests/test_loan_disclosure.py::test_task_0665_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_loan_disclosure_pqc.py::test_task_0665_canonical_record_encoding_is_stable`.
