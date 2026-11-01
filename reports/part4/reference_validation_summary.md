# Reference implementation validation summary

Validation date: 2026-11-01 (Asia/Calcutta)

## Overall result

- Total references: 170
- Passed: 30 (OPMB-0001 through OPMB-0030; REPO-001 through REPO-003)
- Failed: 0
- Pending: 140 (OPMB-0031 through OPMB-0170; REPO-004 through REPO-017)

The 30 tested references are supported by application-level migration suites. Each suite is shared by its application's ten task records; the report does not claim a separate invocation for each task. `reference_patch_status` remains `pending` for suites that contain only skipped placeholder tests.

## Application results

| Repository | Task IDs | Reference migration suite | Original suite | Reference outcome |
|---|---|---:|---:|---|
| REPO-001 SecureVault | OPMB-0001–0010 | 9 passed, exit 0 | 11 passed, exit 0 | Passed |
| REPO-002 KeyLedger | OPMB-0011–0020 | 5 passed, exit 0 | 7 passed, exit 0 | Passed |
| REPO-003 SecurePrint | OPMB-0021–0030 | 5 passed, exit 0 | 6 passed, exit 0 | Passed |
| REPO-004 TrustBridge | OPMB-0031–0040 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-005 FleetUpdate | OPMB-0041–0050 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-006 CareLink | OPMB-0051–0060 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-007 PayRoute | OPMB-0061–0070 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-008 CodeSignHub | OPMB-0071–0080 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-009 EdgeTunnel | OPMB-0081–0090 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-010 ArchiveSeal | OPMB-0091–0100 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-011 DevicePair | OPMB-0101–0110 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-012 BuildRelay | OPMB-0111–0120 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-013 CaseExchange | OPMB-0121–0130 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-014 SensorMesh | OPMB-0131–0140 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-015 IdentityCache | OPMB-0141–0150 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-016 BackupRelay | OPMB-0151–0160 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |
| REPO-017 PolicyGate | OPMB-0161–0170 | 1 skipped, exit 0 | 3 passed, exit 0 | Pending: placeholder only |

Full commands, captured stdout, exit codes, task mappings, and task requirements are recorded in `reports/evidence/REPO-*/reference-validation-execution.json`. The executable runner is `python -m validation.run_reference_suites --all-applications`.

## Findings and remaining work

- REPO-001 through REPO-003 have executable migration suites and passed their tested cases. These suites provide application-level evidence for their ten associated task records apiece; task-specific verification beyond the shared app tests remains a review limitation.
- REPO-004 through REPO-017 have reference folders containing pending/readme placeholders and migration test modules that explicitly skip with “PQC reference implementation is pending; candidate task only.” Their process exit codes are zero because pytest skipped the only test. They are therefore correctly left pending, with no behavior or cryptographic property inferred.
- The original application suites passed for all 17 repositories. This validates the originals only and does not establish any PQC reference behavior for REPO-004 through REPO-017.
- The execution evidence records those fresh original-suite results; existing per-task `original_test_status` metadata was left unchanged for this reference-testing objective.
- REPO-001's manifest incorrectly listed its original test module as `migration_tests`. The manifest and ten task files now point to `tests/test_securevault_pqc.py`; the original suite remains `tests/test_securevault.py`.
- No reference test failures were observed. The remaining 140 implementations still need to be authored, their placeholder tests replaced with requirement-specific executable coverage, and their behavior verified before they can be marked tested.

No task IDs or application identities were changed. No task was accepted or marked verified.
