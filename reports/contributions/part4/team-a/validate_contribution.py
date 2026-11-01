"""Read-only structural and evidence audit for the Team A allocation."""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

from jsonschema import validate

ROOT = Path(__file__).resolve().parents[4]
CONTRIBUTION = ROOT / "reports" / "contributions" / "part4" / "team-a"
EXPECTED_REPOS = [f"REPO-{number:03d}" for number in range(18, 33)]
EXPECTED_TASKS = [f"OPMB-{number:04d}" for number in range(171, 321)]
PROBLEMS: list[str] = []
CHECKS: list[dict] = []


def check(name: str, passed: bool, detail: str = "") -> None:
    CHECKS.append({"check": name, "result": "passed" if passed else "failed", "detail": detail})
    if not passed:
        PROBLEMS.append(f"{name}: {detail}")


def definitions(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        PROBLEMS.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return set()
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
    return names


def normalized(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.casefold()))


def main() -> int:
    repository_schema = json.loads((ROOT / "benchmark/schemas/repository.schema.json").read_text(encoding="utf-8"))
    task_schema = json.loads((ROOT / "benchmark/schemas/task.schema.json").read_text(encoding="utf-8"))
    repository_manifest = json.loads((CONTRIBUTION / "repository_manifest.json").read_text(encoding="utf-8"))
    task_manifest = json.loads((CONTRIBUTION / "task_manifest.json").read_text(encoding="utf-8"))
    evidence_summary = json.loads((CONTRIBUTION / "test_summary.json").read_text(encoding="utf-8"))

    repo_ids = [row["repository_id"] for row in repository_manifest["repositories"]]
    check("15 allocated repositories", repo_ids == EXPECTED_REPOS, f"found {len(repo_ids)}: {repo_ids}")
    base_repositories = json.loads((ROOT / "benchmark/manifests/repositories.json").read_text(encoding="utf-8"))["repositories"]
    new_names = {row["name"].casefold() for row in repository_manifest["repositories"]}
    old_names = {row["name"].casefold() for row in base_repositories}
    new_domains = {row["application_domain"] for row in repository_manifest["repositories"]}
    old_domains = {row["application_domain"] for row in base_repositories}
    check("application names do not collide", not (new_names & old_names), str(sorted(new_names & old_names)))
    check("application domain labels are unique", len(new_domains) == 15)
    check("no exact application-domain collision", not (new_domains & old_domains), str(sorted(new_domains & old_domains)))
    for row in repository_manifest["repositories"]:
        try:
            validate(row, repository_schema)
        except Exception as exc:
            PROBLEMS.append(f"repository schema {row.get('repository_id')}: {exc}")
    check("repository manifest schema", not any("repository schema" in item for item in PROBLEMS))

    tasks = task_manifest["tasks"]
    task_ids = [task["task_id"] for task in tasks]
    check("150 sequential task IDs", task_ids == EXPECTED_TASKS, f"count={len(task_ids)}, unique={len(set(task_ids))}")
    check("task IDs unique", len(task_ids) == len(set(task_ids)))
    for task in tasks:
        try:
            validate(task, task_schema)
        except Exception as exc:
            PROBLEMS.append(f"task schema {task.get('task_id')}: {exc}")
    check("task metadata schema", not any("task schema" in item for item in PROBLEMS))

    canonical = json.loads((ROOT / "benchmark/manifests/tasks.json").read_text(encoding="utf-8"))
    existing_objectives = {normalized(task["migration_objective"]) for task in canonical.get("tasks", [])}
    objectives = [normalized(task["migration_objective"]) for task in tasks]
    check("no duplicate Team A objectives", len(objectives) == len(set(objectives)))
    check("no exact objective collision with base catalogue", not (set(objectives) & existing_objectives))

    task_dirs = []
    code_links_ok = True
    test_links_ok = True
    source_function_map: dict[tuple[str, str], set[str]] = {}
    test_function_map: dict[tuple[str, str], set[str]] = {}
    for repo in EXPECTED_REPOS:
        base = ROOT / "benchmark" / "repositories" / repo
        app_tasks = sorted((base / "tasks").glob("*/task.json"))
        task_dirs.extend(app_tasks)
        check(f"{repo} application layout", (base / "src").is_dir() and (base / "migrated_reference").is_dir() and (base / "tests").is_dir() and len(app_tasks) == 10, f"task files={len(app_tasks)}")
        metadata = json.loads(app_tasks[0].read_text(encoding="utf-8"))
        slug = metadata["repository_name"]
        original_file = f"tests/test_{slug}.py"
        pqc_file = f"tests/test_{slug}_pqc.py"
        original_text = (base / original_file).read_text(encoding="utf-8")
        pqc_text = (base / pqc_file).read_text(encoding="utf-8")
        classical_crypto = (base / "src" / slug / "crypto.py").read_text(encoding="utf-8")
        pqc_crypto = (base / "migrated_reference" / f"{slug}_pqc" / "crypto.py").read_text(encoding="utf-8")
        check(f"{repo} separated candidate/reference tests", f"from {slug} import crypto" in original_text and f"from {slug}_pqc import crypto" in pqc_text and f"{slug}_pqc" not in original_text)
        check(f"{repo} no skipped/placeholder PQC tests", not re.search(r"pytest\.mark\.(?:skip|skipif|xfail)|NotImplementedError|TODO", pqc_text, re.I))
        check(f"{repo} standardized PQC provider algorithms", all(token in pqc_crypto for token in ("MLDSA65PrivateKey", "MLKEM768PrivateKey", "HKDF", "AESGCM")))
        check(f"{repo} distinct classical baseline", all(token in classical_crypto for token in ("rsa.generate_private_key", "PSS", "OAEP", "AESGCM")))
        for path in (base / "src" / slug).glob("*.py"):
            source_function_map[(repo, path.relative_to(base).as_posix())] = definitions(path)
        for path in (base / "migrated_reference" / f"{slug}_pqc").glob("*.py"):
            source_function_map[(repo, path.relative_to(base).as_posix())] = definitions(path)
        test_function_map[(repo, original_file)] = definitions(base / original_file)
        test_function_map[(repo, pqc_file)] = definitions(base / pqc_file)

    for task in tasks:
        repo = task["repository_id"]
        base = ROOT / "benchmark" / "repositories" / repo
        task_dir = ROOT / task["task_path"]
        for required_file in ("task.json", "requirements.md", "expected_behavior.md", "verification.md"):
            if not (task_dir / required_file).is_file():
                PROBLEMS.append(f"{task['task_id']} missing {required_file}")
        for source in task["source_files"]:
            if not (base / source).is_file():
                code_links_ok = False
                PROBLEMS.append(f"{task['task_id']} missing source {source}")
        for source, function in zip(task["source_files"], task["function_names"]):
            if function not in source_function_map.get((repo, source), set()):
                # The function may be placed in another declared source file.
                if not any(function in source_function_map.get((repo, declared), set()) for declared in task["source_files"]):
                    code_links_ok = False
                    PROBLEMS.append(f"{task['task_id']} function {function} absent from declared source files")
        for kind in ("original_tests", "migration_tests"):
            for reference in task[kind]:
                file, _, node = reference.partition("::")
                if not (base / file).is_file() or not node or node not in test_function_map.get((repo, file), set()):
                    test_links_ok = False
                    PROBLEMS.append(f"{task['task_id']} invalid {kind} reference {reference}")
        if task.get("validation_status") != "candidate":
            PROBLEMS.append(f"{task['task_id']} is not candidate status")
    check("task-to-source function links", code_links_ok)
    check("task-to-original/PQC test links", test_links_ok)
    check("all task specification files exist", not any(" missing " in item for item in PROBLEMS))
    check("all tasks remain candidates", not any("is not candidate status" in item for item in PROBLEMS))

    repo_results = {row["repository_id"]: row for row in evidence_summary["repositories"]}
    evidence_ok = True
    for repo in EXPECTED_REPOS:
        result_path = ROOT / "reports" / "evidence" / repo / "test-results.json"
        if repo not in repo_results or not result_path.is_file():
            evidence_ok = False
            PROBLEMS.append(f"{repo} missing execution evidence")
            continue
        result = json.loads(result_path.read_text(encoding="utf-8"))
        for suite_key in ("original_suite", "pqc_reference_suite"):
            suite = result[suite_key]
            if suite["result"] != "passed" or suite["exit_code"] != 0 or suite["passed"] != 10 or suite["failed"] or suite["skipped"] or suite["errors"] or suite["warnings"]:
                evidence_ok = False
                PROBLEMS.append(f"{repo} {suite_key} has non-passing evidence")
    check("all 30 suites have clean execution evidence", evidence_ok)
    check("aggregate test summary complete", evidence_summary.get("status") == "passed" and len(repo_results) == 15)

    contribution_ids = {task["task_id"] for task in task_manifest["tasks"]}
    check("task manifest IDs are allocated only", contribution_ids == set(EXPECTED_TASKS))
    report = {"status": "passed" if not PROBLEMS else "failed", "checks": CHECKS, "problems": PROBLEMS}
    (CONTRIBUTION / "quality_checks.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{report['status']}: {len(CHECKS)} checks, {len(PROBLEMS)} problems")
    for problem in PROBLEMS:
        print(f"- {problem}")
    return 1 if PROBLEMS else 0


if __name__ == "__main__":
    raise SystemExit(main())
