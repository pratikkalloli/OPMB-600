"""Find exact duplicate objectives and flag near-duplicates for human review."""
import json
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def norm(value:str)->str: return " ".join(value.lower().split())
def main()->int:
    tasks=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text(encoding="utf-8")).get("tasks",[]); exact=defaultdict(list)
    for task in tasks: exact[norm(task.get("migration_objective",""))].append(task.get("task_id"))
    duplicates={k:v for k,v in exact.items() if k and len(v)>1}; objectives=[(t.get("task_id"),norm(t.get("migration_objective",""))) for t in tasks]; similar=[]
    for index,(left_id,left) in enumerate(objectives):
        for right_id,right in objectives[index+1:]:
            score=SequenceMatcher(None,left,right).ratio()
            if score>=0.90 and left!=right: similar.append((left_id,right_id,round(score,3)))
    print(f"exact duplicate groups: {len(duplicates)}; near-duplicate pairs for human review (>=0.90): {len(similar)}")
    for ids in duplicates.values(): print("duplicate:",", ".join(ids))
    for left,right,score in similar: print(f"review {left} / {right}: similarity={score}")
    return int(bool(duplicates))
if __name__=="__main__": raise SystemExit(main())
