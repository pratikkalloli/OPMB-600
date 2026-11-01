# Expected behavior

- Preserve the TokenStatusProof workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/token_status_proof/workflow.py, src/token_status_proof/crypto.py; the original test is `tests/test_token_status_proof.py::test_task_1272_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_token_status_proof_pqc.py::test_task_1272_public_key_encoding_round_trips_and_binds_purpose`.
