"""Check tested reference paths and evidence links; never infer acceptance."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main()->int:
    tasks=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text(encoding="utf-8")).get("tasks",[]); errors=[]; tested=0
    for task in tasks:
        status=task.get("reference_patch_status","pending"); path=ROOT/task.get("reference_path","")
        if status in {"tested","verified"}:
            tested+=1
            if not path.is_dir(): errors.append(f"{task.get('task_id')}: reference implementation path missing")
            evidence=task.get("reference_test_evidence")
            if not evidence or not (ROOT/evidence).is_file(): errors.append(f"{task.get('task_id')}: reference test evidence missing")
            scan=task.get("post_migration_scanner_evidence")
            if not scan or not (ROOT/scan).is_file(): errors.append(f"{task.get('task_id')}: post-migration scanner evidence missing")
        if task.get("validation_status")=="accepted" and status!="verified": errors.append(f"{task.get('task_id')}: accepted reference has not been marked reviewed/verified")
    print(f"reference implementations tested: {tested}/{len(tasks)}; errors: {len(errors)}")
    for error in errors: print(error)
    return int(bool(errors))
if __name__=="__main__": raise SystemExit(main())
