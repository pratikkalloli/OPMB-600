# Expected behavior

- Preserve the ReferralPacket workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/referral_packet/workflow.py, src/referral_packet/crypto.py; the original test is `tests/test_referral_packet.py::test_task_0934_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_referral_packet_pqc.py::test_task_0934_domain_schema_and_policy_reject_invalid_records`.
