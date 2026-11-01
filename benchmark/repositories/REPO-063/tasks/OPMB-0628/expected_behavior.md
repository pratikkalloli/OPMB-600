# Expected behavior

- Preserve the ProxyVoteInstruction workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/proxy_vote_instruction/workflow.py, src/proxy_vote_instruction/crypto.py; the original test is `tests/test_proxy_vote_instruction.py::test_task_0628_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_proxy_vote_instruction_pqc.py::test_task_0628_hybrid_envelope_binds_recipient_and_record_context`.
