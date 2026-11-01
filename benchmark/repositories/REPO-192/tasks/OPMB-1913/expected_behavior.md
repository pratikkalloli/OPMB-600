# Expected behavior

- Preserve the MunicipalLicense workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/municipal_license/workflow.py, src/municipal_license/crypto.py; the original test is `tests/test_municipal_license.py::test_task_1913_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_municipal_license_pqc.py::test_task_1913_malformed_serialization_and_wrong_purpose_are_rejected`.
