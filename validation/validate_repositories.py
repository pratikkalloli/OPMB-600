"""Validate repository inventory and required project structure."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main()->int:
 data=json.loads((ROOT/"benchmark/manifests/repositories.json").read_text()); repos=data.get("repositories",[]); errors=[]; ids=[r.get("repository_id") for r in repos]
 if len(ids)!=len(set(ids)): errors.append("duplicate repository IDs")
 for r in repos:
  path=ROOT/r.get("path", "")
  if not path.is_dir(): errors.append(f"{r.get('repository_id')}: directory missing")
  elif not (path/"README.md").is_file(): errors.append(f"{r.get('repository_id')}: README missing")
 print(f"repositories: {len(repos)}; errors: {len(errors)}")
 for e in errors: print(e)
 return bool(errors)
if __name__=="__main__": raise SystemExit(main())
