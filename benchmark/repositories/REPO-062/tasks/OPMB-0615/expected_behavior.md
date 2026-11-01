# Expected behavior

- Preserve the BeneficiaryProof workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/beneficiary_proof/workflow.py, src/beneficiary_proof/crypto.py; the original test is `tests/test_beneficiary_proof.py::test_task_0615_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_beneficiary_proof_pqc.py::test_task_0615_canonical_record_encoding_is_stable`.
