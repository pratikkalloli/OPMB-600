"""Execute separate baseline/reference suites and capture truthful task evidence."""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "reports/contributions/scale600/team-a"
PYTHON = ROOT / ".venv311/Scripts/python.exe"

def counts(output: str) -> dict:
    result = {"passed": 0, "failed": 0, "skipped": 0, "errors": 0, "warnings": 0}
    for label in ("passed", "failed", "skipped", "error", "warning"):
        match = re.search(rf"\b(\d+) {label}(?:s)?\b", output)
        if match:
            key = {"error": "errors", "warning": "warnings"}.get(label, label)
            result[key] = int(match.group(1))
    return result

def run_suite(repo: str, test_path: str, kind: str) -> dict:
    command = [str(PYTHON), "-m", "pytest", test_path, "-q", "-p", "no:cacheprovider"]
    completed = subprocess.run(command, cwd=ROOT / "benchmark/repositories" / repo,
                               text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               encoding="utf-8", errors="replace")
    result = counts(completed.stdout)
    status = "passed" if completed.returncode == 0 and result["passed"] > 0 and not result["skipped"] else "failed" if completed.returncode or result["failed"] or result["errors"] else "pending"
    return {"kind": kind, "command": command, "cwd": f"benchmark/repositories/{repo}",
            "exit_code": completed.returncode, "result": status, **result, "output": completed.stdout}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, required=True, choices=range(1, 19))
    args = parser.parse_args()
    if not PYTHON.is_file(): raise SystemExit(f"Pinned interpreter not found: {PYTHON}")
    repos_manifest = OUT / "repository_contribution_manifest.json"
    tasks_manifest = OUT / "task_contribution_manifest.json"
    repositories = json.loads(repos_manifest.read_text(encoding="utf-8"))
    tasks = json.loads(tasks_manifest.read_text(encoding="utf-8"))
    test_summary_path = OUT / "test_summary.json"
    summary = json.loads(test_summary_path.read_text(encoding="utf-8")) if test_summary_path.exists() else {"repositories": []}
    results = {item["repository_id"]: item for item in summary.get("repositories", [])}
    first = 61 + (args.batch - 1) * 10
    exit_status = 0
    for number in range(first, first + 10):
        repo = f"REPO-{number:03d}"
        item = next(row for row in repositories if row["repository_id"] == repo)
        slug = next(task["repository_name"] for task in tasks if task["repository_id"] == repo)
        original = run_suite(repo, f"tests/test_{slug}.py", "original")
        pqc = run_suite(repo, f"tests/test_{slug}_pqc.py", "pqc_reference")
        record = {"repository_id": repo, "application": slug,
                  "captured_at_utc": datetime.now(timezone.utc).isoformat(),
                  "environment": {"python": subprocess.run([str(PYTHON), "--version"], text=True, capture_output=True).stdout.strip(),
                                  "pytest": subprocess.run([str(PYTHON), "-m", "pytest", "--version"], text=True, capture_output=True).stdout.strip()},
                  "original_suite": original, "pqc_reference_suite": pqc}
        evidence_dir = ROOT / "reports/evidence" / repo
        evidence_dir.mkdir(parents=True, exist_ok=True)
        evidence_file = evidence_dir / "test-results.json"
        evidence_file.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        for task in tasks:
            if task["repository_id"] != repo: continue
            task["original_build_status"] = "passed" if original["result"] == "passed" else "pending"
            task["original_test_status"] = original["result"]
            task["reference_patch_status"] = "tested" if pqc["result"] == "passed" else "pending"
            task["cryptographic_verification_status"] = "passed" if pqc["result"] == "passed" else "pending"
            task["validation_status"] = "candidate"
            task["original_test_evidence"] = f"reports/evidence/{repo}/test-results.json"
            task["reference_test_evidence"] = f"reports/evidence/{repo}/test-results.json"
            task["cryptographic_verification_evidence"] = f"reports/evidence/{repo}/test-results.json"
        results[repo] = {"repository_id": repo,
                         "original": {key: original[key] for key in ("result", "passed", "failed", "skipped", "errors", "warnings", "exit_code")},
                         "pqc_reference": {key: pqc[key] for key in ("result", "passed", "failed", "skipped", "errors", "warnings", "exit_code")},
                         "evidence": f"reports/evidence/{repo}/test-results.json"}
        print(f"{repo}: original {original['result']} {original['passed']}/{original['passed']+original['failed']+original['skipped']}; PQC {pqc['result']} {pqc['passed']}/{pqc['passed']+pqc['failed']+pqc['skipped']}; skipped={original['skipped']+pqc['skipped']} errors={original['errors']+pqc['errors']} warnings={original['warnings']+pqc['warnings']}", flush=True)
        if original["result"] != "passed" or pqc["result"] != "passed": exit_status = 1
    tasks.sort(key=lambda item: item["task_id"])
    repositories.sort(key=lambda item: item["repository_id"])
    summary = {"status": "complete" if len(results) == 180 and all(x["original"]["result"] == x["pqc_reference"]["result"] == "passed" for x in results.values()) else "partial",
               "environment": {"python": "Python 3.11.9", "pytest": "pytest 8.4.2"},
               "repositories_tested": len(results), "repositories_planned": 180,
               "original_passed": sum(row["original"]["passed"] for row in results.values()),
               "pqc_passed": sum(row["pqc_reference"]["passed"] for row in results.values()),
               "repositories": [results[key] for key in sorted(results)]}
    (OUT / "test_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tasks_manifest.write_text(json.dumps(tasks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "repository_contribution_manifest.json").write_text(json.dumps(repositories, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for task in tasks:
        if task["repository_id"] in [f"REPO-{n:03d}" for n in range(first, first + 10)]:
            task_path = ROOT / task["task_path"] / "task.json"
            task_path.write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for filename, suite_key in (("original_test_summary.json", "original"), ("pqc_reference_test_summary.json", "pqc_reference")):
        (OUT / filename).write_text(json.dumps({"suite": suite_key, "repositories_tested": len(results),
             "tests_passed": sum(x[suite_key]["passed"] for x in results.values()),
             "failures": sum(x[suite_key]["failed"] for x in results.values()),
             "skips": sum(x[suite_key]["skipped"] for x in results.values()),
             "errors": sum(x[suite_key]["errors"] for x in results.values()),
             "warnings": sum(x[suite_key]["warnings"] for x in results.values()), "repositories": summary["repositories"]}, indent=2) + "\n", encoding="utf-8")
    progress = ["# Batch progress", "", "| Batch | Applications | Tasks | Original tests | PQC tests | Status |", "|---:|---|---:|---:|---:|---|"]
    for batch in range(1, 19):
        low = 61 + (batch - 1) * 10; high = low + 9
        ids = [f"REPO-{n:03d}" for n in range(low, high + 1)]
        completed = all(repo in results and results[repo]["original"]["result"] == results[repo]["pqc_reference"]["result"] == "passed" for repo in ids)
        orig = sum(results[r]["original"]["passed"] for r in ids if r in results)
        ref = sum(results[r]["pqc_reference"]["passed"] for r in ids if r in results)
        progress.append(f"| {batch:02d} | REPO-{low:03d}–REPO-{high:03d} | 100 | {orig} | {ref} | {'passed' if completed else 'pending'} |")
    (OUT / "batch_progress.md").write_text("\n".join(progress) + "\n", encoding="utf-8")
    return exit_status

if __name__ == "__main__": raise SystemExit(main())
