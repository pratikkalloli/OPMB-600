# Expected behavior

- Preserve the EligibilityCredential workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/eligibility_credential/workflow.py, src/eligibility_credential/crypto.py; the original test is `tests/test_eligibility_credential.py::test_task_1345_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_eligibility_credential_pqc.py::test_task_1345_canonical_record_encoding_is_stable`.
