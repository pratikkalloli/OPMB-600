# Part 3 preflight inventory

Date: 2026-11-01 (Asia/Calcutta)

## Verified starting state

- Git branch: `feature/opmb-600-benchmark` (tracking `origin/feature/opmb-600-benchmark`).
- Existing commits include the benchmark foundation, SecureVault pilot, and KeyLedger. No user changes were present in the working tree at preflight.
- Repository directories and `benchmark/manifests/repositories.json` agree: REPO-001 SecureVault and REPO-002 KeyLedger.
- Task manifest and task directories agree: OPMB-0001 through OPMB-0020, 10 each for the two repositories.
- Both applications have original source, a distinct migrated reference package, original and PQC tests, and README/build metadata.
- The task and repository JSON schemas, four experimental condition configurations, split placeholders, strategy memory schema, evidence files, and validation modules were inspected. The split placeholders remain in place.
- Git history begins with the benchmark foundation and contains work for REPO-001 and REPO-002. This checkout does not contain the prompt's stated 16-app/160-task Parts 1 and 2 inventory.

## Baseline validation

Command: `python -m validation.run_all --allow-incomplete`

- Task links: 20 tasks, 2 linked repositories, 0 errors.
- Duplicate detector: 0 exact duplicate groups and 0 near-duplicate pairs.
- Repository check: 2/60, 0 errors.
- Reference check: 20/20 tested, 0 errors.
- Metadata schema validation could not run because `jsonschema` is not installed.
- The report generator ran and correctly reported 2 repositories, 20 candidate tasks, and 0 accepted tasks.
- `pytest` could not be launched because it is not installed. The configured `python` is MSYS Python with no `pip`; the available Windows Python launch targets could not start. No test results are inferred from earlier checked-in evidence.

## Allocation decision

The next safe identifiers are REPO-003 onward and OPMB-0021 onward. To preserve the requested 15-app/150-task Part 3 size without overwriting existing records, its allocation is REPO-003–REPO-017 and OPMB-0021–OPMB-0170. Therefore suggested names in the prompt are assigned to those next identifiers in order, rather than reusing REPO-017–REPO-031 and OPMB-0161–OPMB-0310. The post-Part-3 inventory target is 17 applications and 170 tasks, with 43 applications and 430 tasks remaining toward OPMB-600.

## Material blockers

- Runtime dependencies are absent from the active Python installation. Dependency installation was attempted through the approved escalation path, but that interpreter has no `pip`; the other installed Python launch targets are inaccessible/missing. Tests and schema validation must remain pending until a usable Python environment with pinned dependencies is available.
- Previous-work inventory discrepancy: Parts 1 and 2 as described in the prompt are not present in this checkout. No missing historical records are fabricated.
