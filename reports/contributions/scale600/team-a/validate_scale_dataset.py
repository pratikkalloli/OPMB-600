"""Audit only Team A's scale allocation; does not mutate shared manifests."""
from __future__ import annotations
import ast, json, re, sys
from collections import Counter
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "reports/contributions/scale600/team-a"

def main() -> int:
    repository_manifest = json.loads((OUT / "repository_contribution_manifest.json").read_text(encoding="utf-8"))
    task_manifest = json.loads((OUT / "task_contribution_manifest.json").read_text(encoding="utf-8"))
    repo_ids = [f"REPO-{number:03d}" for number in range(61, 241)]
    task_ids = [f"OPMB-{number:04d}" for number in range(601, 2401)]
    errors = []
    if [row["repository_id"] for row in repository_manifest] != repo_ids: errors.append("repository manifest must contain REPO-061..REPO-240 exactly once and in order")
    ids = [task["task_id"] for task in task_manifest]
    if len(ids) != len(set(ids)): errors.append("duplicate task IDs")
    if ids != sorted(ids): errors.append("task manifest is not sorted by task ID")
    if any(task_id not in task_ids for task_id in ids): errors.append("task ID outside allocated range")
    schema = json.loads((ROOT / "benchmark/schemas/task.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    counts = Counter(task["repository_id"] for task in task_manifest)
    for repo in repo_ids:
        repo_path = ROOT / "benchmark/repositories" / repo
        app_tasks = [task for task in task_manifest if task["repository_id"] == repo]
        if counts[repo] not in (0, 10): errors.append(f"{repo} has {counts[repo]} tasks")
        if not app_tasks:
            if repo_path.exists(): errors.append(f"{repo} directory exists without task manifest")
            continue
        if not repo_path.is_dir(): errors.append(f"{repo} directory missing")
        for rel in ("README.md", "pyproject.toml", "requirements.txt"):
            if not (repo_path / rel).is_file(): errors.append(f"{repo} missing {rel}")
        slug = app_tasks[0]["repository_name"]
        originals = repo_path / "tests" / f"test_{slug}.py"
        pqc_tests = repo_path / "tests" / f"test_{slug}_pqc.py"
        if not originals.is_file() or not pqc_tests.is_file(): errors.append(f"{repo} test suite missing")
        for suite in (originals, pqc_tests):
            if suite.is_file():
                source = suite.read_text(encoding="utf-8")
                if re.search(r"pytest\.(skip|mark\.skip)|unittest\.skip", source): errors.append(f"{repo} has a skipped test placeholder")
                if "TODO" in source or "pass  #" in source: errors.append(f"{repo} test has placeholder content")
        for task in app_tasks:
            if task["validation_status"] != "candidate": errors.append(f"{task['task_id']} must remain candidate")
            for error in validator.iter_errors(task):
                errors.append(f"{task['task_id']} schema: {error.message}")
            for rel in task["source_files"]:
                if not (repo_path / rel).is_file(): errors.append(f"{task['task_id']} missing source {rel}")
            for ref in task.get("original_tests", []) + task.get("migration_tests", []):
                test_file, node = ref.split("::", 1)
                path = repo_path / test_file
                if not path.is_file() or node not in path.read_text(encoding="utf-8"):
                    errors.append(f"{task['task_id']} missing test node {ref}")
            for function in task["function_names"]:
                method = function.split(".")[-1]
                found = False
                for rel in task["source_files"]:
                    path = repo_path / rel
                    if not path.is_file(): continue
                    try: tree = ast.parse(path.read_text(encoding="utf-8"))
                    except SyntaxError as exc:
                        errors.append(f"{task['task_id']} source parse error in {rel}: {exc}"); continue
                    if any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == method for node in ast.walk(tree)):
                        found = True; break
                if not found: errors.append(f"{task['task_id']} unmapped source function {function}")
    report = {"result": "passed" if not errors else "failed", "repositories_planned": 180,
              "repositories_with_implementation": len({task["repository_id"] for task in task_manifest}),
              "tasks_planned": 1800, "tasks_with_definition": len(task_manifest),
              "tasks_by_repository": counts, "errors": errors}
    report["tasks_by_repository"] = dict(report["tasks_by_repository"])
    (OUT / "quality_checks.json").write_bytes((json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"{report['result']}: {len(task_manifest)} task definitions checked, {len(errors)} problems")
    for error in errors[:30]: print("- " + error)
    return 1 if errors else 0

if __name__ == "__main__": raise SystemExit(main())
