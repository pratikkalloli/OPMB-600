# Expected behavior

- Preserve the FulfillmentProof workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/fulfillment_proof/workflow.py, src/fulfillment_proof/crypto.py; the original test is `tests/test_fulfillment_proof.py::test_task_2268_hybrid_envelope_binds_recipient_and_record_context` and PQC migration test is `tests/test_fulfillment_proof_pqc.py::test_task_2268_hybrid_envelope_binds_recipient_and_record_context`.
