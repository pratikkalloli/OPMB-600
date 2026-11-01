# Expected behavior

- Preserve the DecreeMilestone workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/decree_milestone/workflow.py, src/decree_milestone/crypto.py; the original test is `tests/test_decree_milestone.py::test_task_2077_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_decree_milestone_pqc.py::test_task_2077_signature_rejects_tamper_wrong_key_and_downgrade`.
