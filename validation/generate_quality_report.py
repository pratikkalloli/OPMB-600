"""Generate dataset statistics and quality summaries from actual manifests."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def save(name,data):
    path=ROOT/"benchmark/manifests"/name; path.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
def main()->int:
    repos=json.loads((ROOT/"benchmark/manifests/repositories.json").read_text(encoding="utf-8")).get("repositories",[]); tasks=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text(encoding="utf-8")).get("tasks",[])
    counts=lambda field:dict(Counter(t.get(field,"pending") for t in tasks))
    report={"target":{"repositories":60,"tasks":600},"repository_count":len(repos),"task_count":len(tasks),"accepted_task_count":sum(t.get("validation_status")=="accepted" for t in tasks),"candidate_task_count":sum(t.get("validation_status")=="candidate" for t in tasks),"pending_task_count":sum(t.get("validation_status")=="pending" for t in tasks),"dataset_status":"complete" if len(repos)==60 and len(tasks)==600 and all(t.get("validation_status")=="accepted" for t in tasks) else "incomplete","domains":counts("application_domain"),"migration_families":counts("migration_family"),"difficulty":counts("difficulty"),"original_test_status":counts("original_test_status"),"reference_status":counts("reference_patch_status"),"cryptographic_verification_status":counts("cryptographic_verification_status"),"blockers":[]}
    if len(repos)<60: report["blockers"].append(f"{60-len(repos)} application projects remain to be authored.")
    if len(tasks)<600: report["blockers"].append(f"{600-len(tasks)} migration tasks remain to be authored.")
    if report["accepted_task_count"]<600: report["blockers"].append(f"{600-report['accepted_task_count']} tasks are not accepted; independent review and complete evidence are still required.")
    save("dataset_statistics.json",{"repository_count":len(repos),"task_count":len(tasks),"domains":report["domains"],"migration_families":report["migration_families"],"difficulty":report["difficulty"]})
    save("task_quality_report.json",{"dataset_status":report["dataset_status"],"accepted":report["accepted_task_count"],"candidate":report["candidate_task_count"],"pending":report["pending_task_count"],"original_test_status":report["original_test_status"],"reference_test_status":report["reference_status"],"cryptographic_verification_status":report["cryptographic_verification_status"],"blockers":report["blockers"]})
    save("validation_summary.json",{"inventory_check":"partial" if len(repos)<60 or len(tasks)<600 else "full","repositories_present":len(repos),"tasks_present":len(tasks),"accepted_tasks":report["accepted_task_count"],"note":"Detailed consistency command results are emitted by validation.run_all; this summary does not infer acceptance."})
    out=ROOT/"reports/quality_report.json"; out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
