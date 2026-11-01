# Expected behavior

- Preserve the InspectionCertificate workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/inspection_certificate/workflow.py, src/inspection_certificate/crypto.py; the original test is `tests/test_inspection_certificate.py::test_task_2021_identity_separates_signing_and_transport_keys` and PQC migration test is `tests/test_inspection_certificate_pqc.py::test_task_2021_identity_separates_signing_and_transport_keys`.
