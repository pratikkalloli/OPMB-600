# Expected behavior

- Preserve the PartnerOnboard workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/partner_onboard/workflow.py, src/partner_onboard/crypto.py; the original test is `tests/test_partner_onboard.py::test_task_0896_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_partner_onboard_pqc.py::test_task_0896_signature_binds_record_context_and_validity`.
