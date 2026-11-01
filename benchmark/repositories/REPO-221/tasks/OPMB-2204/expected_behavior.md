# Expected behavior

- Preserve the CatalogOfferProof workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/catalog_offer_proof/workflow.py, src/catalog_offer_proof/crypto.py; the original test is `tests/test_catalog_offer_proof.py::test_task_2204_domain_schema_and_policy_reject_invalid_records` and PQC migration test is `tests/test_catalog_offer_proof_pqc.py::test_task_2204_domain_schema_and_policy_reject_invalid_records`.
