# OPMB-600 progress

## 2026-11-01 inventory checkpoint

- Canonical inventory: 17 applications and 170 candidate tasks across 17 application domains.
- Ten tasks are linked to each application (REPO-001 through REPO-017; OPMB-0001 through OPMB-0170).
- REPO-001 SecureVault, REPO-002 KeyLedger, and REPO-003 SecurePrint have executable original and reference suites with recorded results. REPO-004 through REPO-017 reference suites remain skipped placeholders; 140 task references remain pending.
- No tasks are accepted. Independent review remains outstanding.
- The target is 60 applications and 600 tasks; 43 applications and 430 tasks remain.
- Formal JSON Schema and pytest checks were previously unavailable due to the Python environment. See `reports/part3/part3_audit_report.md` for the audit details and current limitations.

## 2026-11-01 reference test run

- Reran original and PQC migration suites for all 17 applications under Python 3.11.9, pytest 8.4.2, and cryptography 50.0.2.
- REPO-001 through REPO-003 migration suites passed (19 tests total across the three apps). The 140 task records linked to REPO-004 through REPO-017 remain pending because their only migration test is explicitly skipped and their reference folders are placeholders.
- All 17 original suites passed. Full execution output and exit codes are in `reports/evidence/REPO-*/reference-validation-execution.json`; the application/task summary is in `reports/part4/reference_validation_summary.md`.
- `python -m validation.run_all --allow-incomplete` passed all consistency checks. `pytest -q` passed (2 tests). The dataset remains incomplete and no tasks are accepted.
