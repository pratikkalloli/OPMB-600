# Expected behavior

- Preserve the InventoryAllocation workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/inventory_allocation/workflow.py, src/inventory_allocation/crypto.py; the original test is `tests/test_inventory_allocation.py::test_task_2224_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_inventory_allocation_pqc.py::test_task_2224_domain_schema_and_policy_reject_invalid_records`.
