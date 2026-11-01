# Expected behavior

- Preserve the MedicalCertificate workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/medical_certificate/workflow.py, src/medical_certificate/crypto.py; the original test is `tests/test_medical_certificate.py::test_task_1106_signature_binds_record_context_and_validity` and PQC migration test is `tests/test_medical_certificate_pqc.py::test_task_1106_signature_binds_record_context_and_validity`.
