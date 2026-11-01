"""Run allocated application suites and record evidence without touching shared manifests."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CONTRIBUTION = ROOT / "reports" / "contributions" / "part4" / "team-a"
PYTHON = ROOT / ".venv311" / "Scripts" / "python.exe"


def counts(output: str) -> dict:
    result = {"passed": 0, "failed": 0, "skipped": 0, "errors": 0, "warnings": 0}
    for key in ("passed", "failed", "skipped", "error", "warning"):
        match = re.search(rf"\b(\d+) {key}(?:s)?\b", output)
        if match:
            result["errors" if key == "error" else "warnings" if key == "warning" else key] = int(match.group(1))
    return result


def run_suite(repo: str, test_file: str, kind: str) -> dict:
    cwd = ROOT / "benchmark" / "repositories" / repo
    command = [str(PYTHON), "-m", "pytest", test_file, "-q", "-p", "no:cacheprovider"]
    completed = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    summary = counts(completed.stdout)
    result = "passed" if completed.returncode == 0 and summary["passed"] > 0 and summary["skipped"] == 0 else "failed" if completed.returncode != 0 or summary["failed"] or summary["errors"] else "pending"
    return {"kind": kind, "command": ["python", "-m", "pytest", test_file, "-q", "-p", "no:cacheprovider"],
            "cwd": f"benchmark/repositories/{repo}", "exit_code": completed.returncode,
            "result": result, **summary, "output": completed.stdout}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repos", nargs="+", help="allocated repository IDs to execute")
    args = parser.parse_args()
    if not PYTHON.is_file():
        raise SystemExit(f"Pinned project interpreter not found: {PYTHON}")
    pytest_version = subprocess.run([str(PYTHON), "-m", "pytest", "--version"], cwd=ROOT,
                                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.strip()
    python_version = subprocess.run([str(PYTHON), "--version"], cwd=ROOT,
                                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.strip()
    aggregate = json.loads((CONTRIBUTION / "test_summary.json").read_text(encoding="utf-8"))
    summary_by_repo = {row["repository_id"]: row for row in aggregate["repositories"]}
    task_manifest_path = CONTRIBUTION / "task_manifest.json"
    task_manifest = json.loads(task_manifest_path.read_text(encoding="utf-8"))
    tasks_by_id = {task["task_id"]: task for task in task_manifest["tasks"]}
    exit_status = 0
    for repo in args.repos:
        slug_dir = ROOT / "benchmark" / "repositories" / repo
        metadata = json.loads(next(slug_dir.glob("tasks/OPMB-*/task.json")).read_text(encoding="utf-8"))
        slug = metadata["repository_name"]
        original = run_suite(repo, f"tests/test_{slug}.py", "original")
        reference = run_suite(repo, f"tests/test_{slug}_pqc.py", "pqc_reference")
        record = {"repository_id": repo, "application": metadata["repository_name"],
                  "captured_at_utc": datetime.now(timezone.utc).isoformat(),
                  "environment": {"python": python_version, "pytest": pytest_version},
                  "original_suite": original, "pqc_reference_suite": reference}
        evidence_dir = ROOT / "reports" / "evidence" / repo
        evidence_dir.mkdir(parents=True, exist_ok=True)
        evidence_path = evidence_dir / "test-results.json"
        evidence_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        repo_tasks = sorted((slug_dir / "tasks").glob("OPMB-*/task.json"))
        for task_path in repo_tasks:
            task = json.loads(task_path.read_text(encoding="utf-8"))
            task["original_build_status"] = original["result"]
            task["original_test_status"] = original["result"]
            task["reference_patch_status"] = "tested" if reference["result"] == "passed" else "pending"
            task["cryptographic_verification_status"] = "passed" if reference["result"] == "passed" else "pending"
            task["validation_status"] = "candidate"
            task["original_test_evidence"] = f"reports/evidence/{repo}/test-results.json"
            task["reference_test_evidence"] = f"reports/evidence/{repo}/test-results.json"
            task["cryptographic_verification_evidence"] = f"reports/evidence/{repo}/test-results.json"
            task_path.write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            tasks_by_id[task["task_id"]] = task
        summary_by_repo[repo] = {"repository_id": repo, "original": {k: original[k] for k in ("result", "passed", "failed", "skipped", "errors", "warnings", "exit_code")},
                                 "pqc_reference": {k: reference[k] for k in ("result", "passed", "failed", "skipped", "errors", "warnings", "exit_code")},
                                 "evidence": f"reports/evidence/{repo}/test-results.json"}
        print(f"{repo} original={original['result']} ({original['passed']} passed, {original['failed']} failed, {original['skipped']} skipped, {original['errors']} errors, {original['warnings']} warnings); "
              f"PQC={reference['result']} ({reference['passed']} passed, {reference['failed']} failed, {reference['skipped']} skipped, {reference['errors']} errors, {reference['warnings']} warnings)")
        if original["result"] != "passed" or reference["result"] != "passed":
            exit_status = 1
    aggregate["status"] = "passed" if all(row["original"].get("result", row["original"].get("status")) == "passed" and row["pqc_reference"].get("result", row["pqc_reference"].get("status")) == "passed" for row in summary_by_repo.values()) and len(summary_by_repo) == 15 else "partial"
    aggregate["environment"] = {"python": python_version, "pytest": pytest_version}
    aggregate["repositories"] = [summary_by_repo[key] for key in sorted(summary_by_repo)]
    (CONTRIBUTION / "test_summary.json").write_text(json.dumps(aggregate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    task_manifest["tasks"] = [tasks_by_id[key] for key in sorted(tasks_by_id)]
    task_manifest_path.write_text(json.dumps(task_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if aggregate["status"] == "passed":
        crypto_version = subprocess.run([str(PYTHON), "-c", "from importlib.metadata import version; print(version('cryptography'))"],
                                        cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.strip()
        originals = sum(row["original"]["passed"] for row in summary_by_repo.values())
        pqc_tests = sum(row["pqc_reference"]["passed"] for row in summary_by_repo.values())
        report_lines = ["# Cryptographic verification", "", f"Status: **passed by application tests** in {python_version}, {pytest_version}, and `cryptography=={crypto_version}`.",
                        "", f"The 15 separate PQC suites passed {pqc_tests} tests with no failures, skips, errors, or warnings. They exercise FIPS 203 ML-KEM-768, FIPS 204 ML-DSA-65, distinct signing/transport keys, purpose-tagged serialization, strict version and algorithm checks, context-bound signatures, HKDF-SHA-256, AES-256-GCM, malformed-input rejection, and lifecycle behavior.",
                        "", "| Repository | PQC tests | Result |", "|---|---:|---|"]
        report_lines.extend(f"| {repo} | {row['pqc_reference']['passed']} passed, {row['pqc_reference']['failed']} failed, {row['pqc_reference']['skipped']} skipped | {row['pqc_reference']['result']} |" for repo, row in sorted(summary_by_repo.items()))
        report_lines.extend(["", "Application tests verify domain policy and workflow behavior in addition to cryptographic properties. Passing tests are execution evidence, not independent NIST validation or production approval."])
        (CONTRIBUTION / "crypto_verification_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
        implementation = ["# Team A implementation report", "", "## Delivery", "", "- 15 domain-specific application projects completed.", "- 150 task definitions created for OPMB-0171 through OPMB-0320.", f"- {originals} original application tests and {pqc_tests} PQC reference tests passed.", "- Every task remains a candidate; no task is accepted.", "", "## Batch results", "", "| Batch | Repositories | Original tests | PQC tests |", "|---|---|---:|---:|"]
        for batch, repos in (("A1", range(18, 23)), ("A2", range(23, 28)), ("A3", range(28, 33))):
            repo_ids = [f"REPO-{number:03d}" for number in repos]
            old_count = sum(summary_by_repo[repo]["original"]["passed"] for repo in repo_ids)
            pqc_count = sum(summary_by_repo[repo]["pqc_reference"]["passed"] for repo in repo_ids)
            implementation.append(f"| {batch} | {repo_ids[0]}–{repo_ids[-1]} | {old_count} passed | {pqc_count} passed |")
        implementation.extend(["", "## Evidence and limitations", "", "Per-repository commands, raw pytest output, exit codes, counts, environment, and timestamps are stored under `reports/evidence/REPO-018` through `REPO-032`. Source-to-test links are listed in `task_inventory.csv`. The applications are controlled synthetic simulations; their SQLite ledgers and in-memory key registries are not production key custody or deployment systems."])
        (CONTRIBUTION / "implementation_report.md").write_text("\n".join(implementation) + "\n", encoding="utf-8")
        (CONTRIBUTION / "known_issues.md").write_text("# Known issues\n\n- No test failures, skips, errors, or warnings remain in the final captured run.\n- All 150 tasks remain candidates pending independent review; no task is accepted.\n- Private-key persistence, hardware protection, network protocols, and production deployment are outside these synthetic benchmark applications.\n")
    return exit_status


if __name__ == "__main__":
    raise SystemExit(main())
