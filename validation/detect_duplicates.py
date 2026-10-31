"""Detect exact duplicate task objectives and descriptions."""
import json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main()->int:
 tasks=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text()).get("tasks",[]); groups=defaultdict(list)
 for t in tasks:
  key=" ".join(t.get("migration_objective","").lower().split()); groups[key].append(t.get("task_id"))
 duplicates={k:v for k,v in groups.items() if k and len(v)>1}
 print(f"duplicate objective groups: {len(duplicates)}")
 for k,v in duplicates.items(): print(f"{v}: {k}")
 return bool(duplicates)
if __name__=="__main__": raise SystemExit(main())
