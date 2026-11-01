# Expected behavior

- Preserve the MunicipalLicense workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/municipal_license/workflow.py, src/municipal_license/crypto.py; the original test is `tests/test_municipal_license.py::test_task_1912_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_municipal_license_pqc.py::test_task_1912_public_key_encoding_round_trips_and_binds_purpose`.
