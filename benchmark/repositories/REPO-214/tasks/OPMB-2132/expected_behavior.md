# Expected behavior

- Preserve the WarrantyClaim workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/warranty_claim/workflow.py, src/warranty_claim/crypto.py; the original test is `tests/test_warranty_claim.py::test_task_2132_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_warranty_claim_pqc.py::test_task_2132_public_key_encoding_round_trips_and_binds_purpose`.
