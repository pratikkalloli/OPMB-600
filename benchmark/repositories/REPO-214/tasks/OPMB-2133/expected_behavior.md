# Expected behavior

- Preserve the WarrantyClaim workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/warranty_claim/workflow.py, src/warranty_claim/crypto.py; the original test is `tests/test_warranty_claim.py::test_task_2133_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_warranty_claim_pqc.py::test_task_2133_malformed_serialization_and_wrong_purpose_are_rejected`.
