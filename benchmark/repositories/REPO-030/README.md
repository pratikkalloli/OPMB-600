# ApprovalFlow

Controlled synthetic application for OPMB-600. Multi-stage approval signatures and quorum verification. Classical baseline: RSA-3072 PSS and RSA-OAEP/AES-256-GCM. The independent reference package uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM.

**Scope distinction:** implements multi-approver request-stage quorums; it is distinct from delegated policy-bundle approval and authorization decisions.

Original source is in `src/approvalflow/`; the migration reference is in `migrated_reference/approvalflow_pqc/`. Both implement the domain-specific `approval request` model and workflow, strict field validation, a persistent SQLite signed-record ledger, a runnable CLI, key serialization, and key lifecycle.

From this directory, run the original CLI with `PYTHONPATH=src python -m approvalflow [record.json]` on POSIX or `$env:PYTHONPATH='src'; python -m approvalflow [record.json]` in PowerShell. For the separate reference CLI, set `PYTHONPATH=migrated_reference` (PowerShell: `$env:PYTHONPATH='migrated_reference'`) and run `python -m approvalflow_pqc [record.json]`. Omit the file to read JSON from standard input. Run the two test suites with `python -m pytest tests/test_approvalflow.py -q` and `python -m pytest tests/test_approvalflow_pqc.py -q`. This synthetic benchmark is not a production system.
