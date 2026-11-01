"""Generate Part 3 summaries from manifests and captured checks."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/part3"
OUT.mkdir(parents=True, exist_ok=True)
repos = json.loads((ROOT / "benchmark/manifests/repositories.json").read_text(encoding="utf-8"))["repositories"]
tasks = json.loads((ROOT / "benchmark/manifests/tasks.json").read_text(encoding="utf-8"))["tasks"]
part_repos = [r for r in repos if r["repository_id"] == "REPO-003"]
part_tasks = [t for t in tasks if t["repository_id"] == "REPO-003"]

with (OUT / "application_inventory.csv").open("w", newline="", encoding="utf-8") as f:
    fields = ["repository_id", "name", "application_domain", "path", "task_count", "status", "test_status", "reference_test_status"]
    writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
    for r in part_repos: writer.writerow({key: r.get(key, "") for key in fields})
with (OUT / "task_inventory.csv").open("w", newline="", encoding="utf-8") as f:
    fields = ["task_id", "repository_id", "repository_name", "migration_family", "migration_target", "migration_objective", "validation_status", "original_test_status", "reference_patch_status", "cryptographic_verification_status"]
    writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
    for task in part_tasks: writer.writerow({key: task.get(key, "") for key in fields})

scan_path = ROOT / "reports/evidence/REPO-003/post-migration-scan.json"
scan = json.loads(scan_path.read_text(encoding="utf-8")) if scan_path.is_file() else None
outputs = {
    "test_summary.json": {"repository_id": "REPO-003", "original_tests": {"status": "not_run", "reason": "cryptography and pytest unavailable"}, "pqc_reference_tests": {"status": "not_run", "reason": "cryptography and pytest unavailable"}, "syntax_compilation": {"status": "passed", "command": "python -m compileall -q benchmark/repositories/REPO-003"}, "test_counts": {"original_passed": None, "original_failed": None, "reference_passed": None, "reference_failed": None}, "accepted_tasks": 0, "candidate_tasks": len(part_tasks)},
    "metadata_validation.json": {"status": "blocked", "task_link_check": "passed: 30 tasks / 3 repositories / 0 errors", "repository_check": "passed: 3 repositories / 0 errors", "jsonschema_check": "not_run: jsonschema unavailable; no schema result claimed", "part3_repositories": len(part_repos), "part3_tasks": len(part_tasks), "unique_task_ids": len({t["task_id"] for t in part_tasks}) == len(part_tasks), "task_statuses": sorted({t["validation_status"] for t in part_tasks})},
    "crypto_scan_summary.json": {"repository_id": "REPO-003", "scanner": "pqc_agent.scanner.scan_python", "scan_path": "migrated_reference/secureprint_pqc", "findings": len(scan["findings"]) if scan else None, "scope": scan["classical_public_key_families_scanned"] if scan else [], "limitations": scan["scope_limit"] if scan else "Scanner not run"}
}
for name, data in outputs.items(): (OUT / name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
(OUT / "implementation_summary.md").write_text(f"""# Part 3 implementation summary

Starting inventory in this checkout: 2 repositories and 20 tasks, not the prompt's expected 16 and 160. This pass implemented {len(part_repos)} application and {len(part_tasks)} candidate tasks: REPO-003 SecurePrint, OPMB-0021–OPMB-0030. The requested 15 applications and 150 tasks are incomplete.

SecurePrint contains original RSA/AES-GCM workflows, a separate ML-KEM-768/HKDF/AES-GCM and ML-DSA-65 reference, source tests, and ten candidate migration records. Source syntax compilation passed. Runtime tests were not run because cryptography/pytest are unavailable and the Windows Python targets could not be started. No tasks are accepted. The reference lexical scanner reported {len(scan['findings']) if scan else 'no recorded'} findings.

Current total: {len(repos)} applications and {len(tasks)} tasks. Remaining toward OPMB-600: {60-len(repos)} applications and {600-len(tasks)} tasks. IDs follow the safe continuation allocation REPO-003 / OPMB-0021.
""", encoding="utf-8")
(OUT / "known_issues.md").write_text("""# Part 3 known issues

- Preflight differs from the prompt: only two prior applications and 20 tasks were present. Safe new allocation starts at REPO-003 / OPMB-0021.
- Only REPO-003 is implemented here; 14 applications and 140 Part 3 tasks remain incomplete.
- Runtime tests and cryptographic execution checks are pending because the active Python lacks cryptography, pytest, and pip; the other Windows Python launch targets were inaccessible.
- JSON Schema validation is pending because jsonschema is unavailable. Task-link, repository, duplicate, syntax, and lexical-scan checks did run.
- Lexical scanning is not a proof of cryptographic correctness and does not inspect dependencies or dynamic code.
- SecurePrint has in-memory records and process-ephemeral keys; it is a research simulation.
- No changes were committed or pushed.
""", encoding="utf-8")
(OUT / "quality_review.md").write_text("""# Part 3 quality review

- Verified start: 2 applications / 20 tasks; prompt expected 16 / 160.
- REPO-003 has separate original and PQC packages plus original/reference test files.
- Ten candidate tasks have unique IDs and source/function references; task validation passed.
- Repository validation passed (3/60, zero errors); duplicate detection reported zero exact and near duplicates.
- Source syntax compilation passed.
- Runtime tests, cryptographic execution, serialization execution, and JSON Schema validation were not run because dependencies and a usable Python install are unavailable.
- PQC reference lexical scan found zero targeted classical public-key calls, subject to scanner limitations.
- Accepted tasks: zero. Split placeholders remain unchanged. Commit/push: none.
""", encoding="utf-8")
