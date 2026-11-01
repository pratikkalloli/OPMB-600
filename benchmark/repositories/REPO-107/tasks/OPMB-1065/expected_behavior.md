# Expected behavior

- Preserve the ProviderLicenseProof workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/provider_license_proof/workflow.py, src/provider_license_proof/crypto.py; the original test is `tests/test_provider_license_proof.py::test_task_1065_canonical_record_encoding_is_stable` and PQC migration test is `tests/test_provider_license_proof_pqc.py::test_task_1065_canonical_record_encoding_is_stable`.
