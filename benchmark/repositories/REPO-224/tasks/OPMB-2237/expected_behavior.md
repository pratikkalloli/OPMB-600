# Expected behavior

- Preserve the DropShipHandoff workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/drop_ship_handoff/workflow.py, src/drop_ship_handoff/crypto.py; the original test is `tests/test_drop_ship_handoff.py::test_task_2237_signature_rejects_tamper_wrong_key_and_downgrade` and PQC migration test is `tests/test_drop_ship_handoff_pqc.py::test_task_2237_signature_rejects_tamper_wrong_key_and_downgrade`.
