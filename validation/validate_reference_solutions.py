"""Ensure reference solutions are explicitly tracked and not claimed without evidence."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main()->int:
 tasks=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text()).get("tasks",[]); errors=[]
 for t in tasks:
  path=ROOT/t.get("reference_path", "")
  if t.get("reference_patch_status")=="verified" and not path.exists(): errors.append(f"{t.get('task_id')}: verified reference missing")
 print(f"reference tasks: {len(tasks)}; errors: {len(errors)}; verified claims remain prohibited pending execution evidence")
 for e in errors: print(e)
 return bool(errors)
if __name__=="__main__": raise SystemExit(main())
