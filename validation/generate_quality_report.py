"""Generate an honest quality report from current manifests."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main()->int:
 repos=json.loads((ROOT/"benchmark/manifests/repositories.json").read_text()).get("repositories",[]); tasks=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text()).get("tasks",[]); report={"repository_count":len(repos),"task_count":len(tasks),"accepted_task_count":sum(t.get("validation_status")=="accepted" for t in tasks),"pending_task_count":sum(t.get("validation_status") in ("candidate","pending") for t in tasks),"domains":dict(Counter(t.get("application_domain","unknown") for t in tasks)),"migration_families":dict(Counter(t.get("migration_family","unknown") for t in tasks)),"difficulty":dict(Counter(t.get("difficulty","unknown") for t in tasks)),"original_test_status":dict(Counter(t.get("original_test_status","unknown") for t in tasks)),"reference_status":dict(Counter(t.get("reference_patch_status","unknown") for t in tasks)),"accepted_status":"incomplete","blockers":["No application projects or task specifications are present yet.","Full 60-project/600-task corpus has not been authored.","Reference migrations and cryptographic verification have not yet been executed.","Repository-level splits are empty and pending.","Isolated execution and post-migration cryptographic scanning are not implemented."]}
 out=ROOT/"reports/quality_report.json"; out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
