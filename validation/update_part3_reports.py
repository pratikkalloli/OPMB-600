import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
repos=json.loads((ROOT/"benchmark/manifests/repositories.json").read_text(encoding="utf-8"))["repositories"]
tasks=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text(encoding="utf-8"))["tasks"]
with (ROOT/"reports/part3/application_inventory.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["repository_id","name","application_domain","path","task_count","status","test_status","reference_test_status"])
    for r in repos: w.writerow([r["repository_id"],r["name"],r["application_domain"],r["path"],r["task_count"],r["status"],r.get("test_status","pending"),r.get("reference_test_status","pending")])
with (ROOT/"reports/part3/task_inventory.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["task_id","repository_id","repository_name","migration_family","migration_target","migration_objective","validation_status","original_test_status","reference_patch_status","cryptographic_verification_status"])
    for t in tasks: w.writerow([t["task_id"],t["repository_id"],t["repository_name"],t["migration_family"],t["migration_target"],t["migration_objective"],t["validation_status"],t["original_test_status"],t["reference_patch_status"],t["cryptographic_verification_status"]])
print(f"Updated Part 3 inventories: {len(repos)} applications, {len(tasks)} tasks.")
