# ToolChangeAuthorization

Authorizes a specific cutting-tool change at a machine cell with a reason code and technician identity before the cell resumes production.

Workflow: Tool wear report, technician assignment, supervisor authorization, change confirmation, and return-to-service.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_tool_change_authorization.py` and `python -m pytest tests/test_tool_change_authorization_pqc.py` from this directory.

## Domain workflow

The original and PQC service layers expose `return_tool_to_service`. This operation verifies the current signed record, enforces the application's business-specific policy, and records the resulting decision and evidence transactionally.
