# Expected behavior

- Preserve the MedicalCertificate workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/medical_certificate/workflow.py, src/medical_certificate/crypto.py; the original test is `tests/test_medical_certificate.py::test_task_1103_malformed_serialization_and_wrong_purpose_are_rejected` and PQC migration test is `tests/test_medical_certificate_pqc.py::test_task_1103_malformed_serialization_and_wrong_purpose_are_rejected`.
