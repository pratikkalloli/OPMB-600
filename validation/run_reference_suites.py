"""Run each pending repository's declared reference migration suite.

The benchmark defines migration tests at application level. Results are
therefore recorded once per repository and linked to that repository's task
IDs without claiming a separate invocation for every task.
"""
from __future__ import annotations

import json
import argparse
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "benchmark/manifests/tasks.json"
REPORT_PATH = ROOT / "reports/part4/reference_validation_results.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-applications", action="store_true",
                        help="rerun application suites even when task references are already tested")
    args = parser.parse_args()
    manifest = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    groups: dict[str, list[dict]] = defaultdict(list)
    for task in manifest.get("tasks", []):
        if args.all_applications or task.get("reference_patch_status") not in {"tested", "verified"}:
            groups[task["repository_id"]].append(task)

    existing = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    previous = {row["task_id"]: row for row in existing.get("results", [])}
    app_results = []
    for repository_id in sorted(groups):
        tasks = groups[repository_id]
        repository = ROOT / "benchmark/repositories" / repository_id
        migration_files = sorted({f for task in tasks for f in task.get("migration_tests", [])})
        original_files = sorted({f for task in tasks for f in task.get("original_tests", [])})
        result = {"repository_id": repository_id,
                  "application": tasks[0].get("repository_name"),
                  "task_ids": [task["task_id"] for task in tasks],
                  "reference_paths": sorted({task.get("reference_path") for task in tasks}),
                  "task_requirements": {task["task_id"]: task.get("migration_requirements", []) for task in tasks},
                  "migration_suite": {"command": [sys.executable, "-m", "pytest", *migration_files, "-q", "-rs"]},
                  "original_suite": {"command": [sys.executable, "-m", "pytest", *original_files, "-q"]}}
        for key, files in (("migration_suite", migration_files), ("original_suite", original_files)):
            command = result[key]["command"]
            completed = subprocess.run(command, cwd=repository, text=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            passed_match = re.search(r"(\d+) passed", completed.stdout)
            skipped_match = re.search(r"(\d+) skipped", completed.stdout)
            failed_match = re.search(r"(\d+) failed", completed.stdout)
            passed_count = int(passed_match.group(1)) if passed_match else 0
            skipped_count = int(skipped_match.group(1)) if skipped_match else 0
            failed_count = int(failed_match.group(1)) if failed_match else 0
            suite_result = ("failed" if completed.returncode != 0 or failed_count else
                            "passed" if passed_count > 0 and skipped_count == 0 else "pending")
            result[key].update({"exit_code": completed.returncode,
                                "result": suite_result,
                                "passed": passed_count, "skipped": skipped_count,
                                "failed": failed_count, "output": completed.stdout})
            print(f"{repository_id} {key}: exit {completed.returncode}")
            print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")

        passed = result["migration_suite"]["result"] == "passed"
        suite_failed = result["migration_suite"]["result"] == "failed"
        evidence_path = f"reports/evidence/{repository_id}/reference-validation-execution.json"
        evidence = ROOT / evidence_path
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["evidence"] = evidence_path
        app_results.append(result)
        for task in tasks:
            task_id = task["task_id"]
            previous[task_id] = {
                "task_id": task_id, "application": task.get("repository_name"),
                "repository_id": repository_id, "reference_path": task.get("reference_path"),
                "reference_patch_status": "tested" if passed else "pending",
                "migration_target": task.get("migration_target"),
                "result": "passed" if passed else "failed" if suite_failed else "pending",
                "reference_suite": result["migration_suite"]["result"],
                "imports_and_runtime": "passed" if passed else "failed" if suite_failed else "not_exercised",
                "cryptographic_migration": "covered_by_application_suite" if passed else "unresolved",
                "syntax_compilation": "covered_by_runtime_imports",
                "evidence": evidence_path,
                "blocker": None if passed else (f"Migration suite exited {result['migration_suite']['exit_code']}" if suite_failed else "Migration suite contains skipped placeholder tests; implementation behavior not exercised."),
                "note": "Application-level migration suite is shared by the listed task records; not a separate invocation per task.",
            }
            if passed:
                task["reference_patch_status"] = "tested"
                task["reference_test_evidence"] = evidence_path
                scanner_path = f"reports/evidence/{repository_id}/post-migration-scan.json"
                if (ROOT / scanner_path).is_file():
                    task["post_migration_scanner_evidence"] = scanner_path
            elif suite_failed:
                task["reference_patch_status"] = "pending"
                task.pop("reference_test_evidence", None)
            else:
                task["reference_patch_status"] = "pending"
                task.pop("reference_test_evidence", None)

    tasks = manifest.get("tasks", [])
    counts = {"total": len(tasks),
              "tested": sum(t.get("reference_patch_status") in {"tested", "verified"} for t in tasks),
              "passed": sum(previous.get(t["task_id"], {}).get("result") == "passed" for t in tasks),
              "failed": sum(previous.get(t["task_id"], {}).get("result") == "failed" for t in tasks),
              "pending": sum(t.get("reference_patch_status") not in {"tested", "verified"} for t in tasks)}
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps({
        "validation_date": date.today().isoformat(), "counts": counts,
        "environment": {"python": sys.version, "executable": sys.executable,
                        "pytest": subprocess.run([sys.executable, "-m", "pytest", "--version"],
                                                  text=True, stdout=subprocess.PIPE,
                                                  stderr=subprocess.STDOUT).stdout.strip()},
        "application_results": app_results,
        "results": [previous[t["task_id"]] for t in tasks],
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    TASKS_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Reference validation counts: {counts}")
    return int(any(row["migration_suite"]["exit_code"] != 0 for row in app_results))


if __name__ == "__main__":
    raise SystemExit(main())
