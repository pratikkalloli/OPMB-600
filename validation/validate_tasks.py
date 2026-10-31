"""Validate task fields, links, tests, evidence, and status consistency."""
from __future__ import annotations
import ast
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={"task_id","repository_id","repository_name","application_domain","repository_version","language","classical_algorithm","cryptographic_operation","source_files","function_names","migration_family","migration_target","migration_objective","preconditions","expected_behavior","migration_requirements","original_tests","verification_procedure","difficulty","original_build_status","original_test_status","reference_patch_status","cryptographic_verification_status","validation_status","known_limitations","created_by"}
EVIDENCE_FIELDS={"original_test_status":"original_test_evidence","reference_patch_status":"reference_test_evidence","cryptographic_verification_status":"cryptographic_verification_evidence"}
def main()->int:
    task_data=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text(encoding="utf-8")); repo_data=json.loads((ROOT/"benchmark/manifests/repositories.json").read_text(encoding="utf-8"))
    repos={r["repository_id"]:r for r in repo_data.get("repositories",[])}; tasks=task_data.get("tasks",[]); errors=[]; counts={}; ids=[]; seen_operations=set()
    for t in tasks:
        tid=t.get("task_id", "<missing>"); ids.append(t.get("task_id")); rid=t.get("repository_id"); counts[rid]=counts.get(rid,0)+1
        missing=REQUIRED-set(t)
        if missing: errors.append(f"{tid}: missing fields {sorted(missing)}")
        repo=repos.get(rid)
        if not repo: errors.append(f"{tid}: unknown repository {rid}"); continue
        base=ROOT/repo.get("path",""); task_dir=ROOT/t.get("task_path","")
        if not task_dir.is_dir(): errors.append(f"{tid}: task directory missing")
        elif not (task_dir/"task.json").is_file(): errors.append(f"{tid}: task.json missing")
        source_defs=set()
        for source in t.get("source_files",[]):
            source_path=base/source
            if not source_path.is_file(): errors.append(f"{tid}: source missing: {source}"); continue
            try:
                tree=ast.parse(source_path.read_text(encoding="utf-8"))
                source_defs.update(node.name for node in ast.walk(tree) if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)))
            except (SyntaxError,UnicodeError) as exc: errors.append(f"{tid}: source parse failed: {source}: {exc}")
        for name in t.get("function_names",[]):
            if name not in source_defs: errors.append(f"{tid}: function/class not found in source_files: {name}")
        for test in t.get("original_tests",[]):
            if not (base/test).is_file(): errors.append(f"{tid}: original test missing: {test}")
        for test in t.get("migration_tests",[]):
            if not (base/test).is_file(): errors.append(f"{tid}: migration test missing: {test}")
        if not (ROOT/t.get("reference_path","")).is_dir(): errors.append(f"{tid}: reference implementation path missing")
        for field in ("migration_objective","expected_behavior","migration_requirements","original_tests","verification_procedure"):
            if not t.get(field): errors.append(f"{tid}: empty {field}")
        for status_field,evidence_field in EVIDENCE_FIELDS.items():
            status=t.get(status_field,"pending")
            if status in {"passed","tested","verified"}:
                evidence=t.get(evidence_field)
                if not evidence or not (ROOT/evidence).is_file(): errors.append(f"{tid}: {status_field} claims {status} without evidence")
        if t.get("validation_status")=="accepted" and not all(t.get(k) in {"passed","tested","verified"} for k in EVIDENCE_FIELDS):
            errors.append(f"{tid}: accepted without all original/reference/crypto evidence")
        for fn in t.get("function_names",[]):
            key=(rid,fn)
            if key in seen_operations: errors.append(f"{tid}: operation function reused by another task: {fn}")
            seen_operations.add(key)
    if len(ids)!=len(set(ids)): errors.append("duplicate task IDs")
    if any(n!=10 for n in counts.values()): errors.append("each represented repository must have exactly ten tasks")
    print(f"tasks: {len(tasks)}; linked repositories: {len(counts)}; errors: {len(errors)}")
    for error in errors: print(error)
    return int(bool(errors))
if __name__=="__main__": raise SystemExit(main())
