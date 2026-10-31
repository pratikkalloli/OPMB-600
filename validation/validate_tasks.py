"""Check task inventory, links, required content, and declared statuses."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXPECTED={"task_id","repository_id","repository_name","application_domain","repository_version","language","classical_algorithm","cryptographic_operation","source_files","function_names","migration_family","migration_target","migration_objective","preconditions","expected_behavior","migration_requirements","original_tests","verification_procedure","difficulty","original_build_status","original_test_status","reference_patch_status","cryptographic_verification_status","validation_status","known_limitations","created_by"}
def main()->int:
 data=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text()); repos={x["repository_id"]:x for x in json.loads((ROOT/"benchmark/manifests/repositories.json").read_text()).get("repositories",[])}; tasks=data.get("tasks",[]); errors=[]
 ids=[t.get("task_id") for t in tasks]
 if len(ids)!=len(set(ids)): errors.append("duplicate task IDs")
 counts={}
 for t in tasks:
  rid=t.get("repository_id"); counts[rid]=counts.get(rid,0)+1
  missing=EXPECTED-set(t)
  if missing: errors.append(f"{t.get('task_id')}: missing fields {sorted(missing)}")
  repo=repos.get(rid)
  if not repo: errors.append(f"{t.get('task_id')}: unknown repository {rid}"); continue
  base=ROOT/repo.get("path", "")
  task_dir=ROOT/t.get("task_path", "")
  if not task_dir.is_dir(): errors.append(f"{t.get('task_id')}: missing task directory")
  for source in t.get("source_files",[]):
   if not (base/source).is_file(): errors.append(f"{t.get('task_id')}: missing source {source}")
  for field in ("migration_objective","original_tests","verification_procedure"):
   if not t.get(field): errors.append(f"{t.get('task_id')}: empty {field}")
  statuses=[t.get(k) for k in ("original_build_status","original_test_status","reference_patch_status","cryptographic_verification_status","validation_status")]
  if any(s in ("passed","accepted","verified") for s in statuses): errors.append(f"{t.get('task_id')}: unsupported claimed result; evidence workflow not configured")
 if tasks and any(n!=10 for n in counts.values()): errors.append("repository task counts are not uniformly ten")
 print(f"tasks: {len(tasks)}; linked repositories: {len(counts)}; errors: {len(errors)}")
 for e in errors: print(e)
 return bool(errors)
if __name__=="__main__": raise SystemExit(main())
