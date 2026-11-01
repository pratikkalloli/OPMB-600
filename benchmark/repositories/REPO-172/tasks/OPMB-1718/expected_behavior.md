# Expected behavior

- Preserve the DegreeEquivalence workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/degree_equivalence/workflow.py, src/degree_equivalence/crypto.py; the original test is `tests/test_degree_equivalence.py::test_task_1718_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_degree_equivalence_pqc.py::test_task_1718_hybrid_envelope_binds_recipient_and_record_context`.
