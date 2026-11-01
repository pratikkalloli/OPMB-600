# Expected behavior

- Preserve the InventoryAllocation workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/inventory_allocation/workflow.py, src/inventory_allocation/crypto.py; the original test is `tests/test_inventory_allocation.py::test_task_2222_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_inventory_allocation_pqc.py::test_task_2222_public_key_encoding_round_trips_and_binds_purpose`.
