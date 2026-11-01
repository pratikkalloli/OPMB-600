# Expected behavior

- Preserve the VerifierKeyCache workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/verifier_key_cache/workflow.py, src/verifier_key_cache/crypto.py; the original test is `tests/test_verifier_key_cache.py::test_task_1429_rotation_retires_old_key_version` and PQC migration test is `tests/test_verifier_key_cache_pqc.py::test_task_1429_rotation_retires_old_key_version`.
