"""Check application directory inventory and project files."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main()->int:
    data=json.loads((ROOT/"benchmark/manifests/repositories.json").read_text(encoding="utf-8")); repos=data.get("repositories",[]); errors=[]; ids=[r.get("repository_id") for r in repos]
    if len(ids)!=len(set(ids)): errors.append("duplicate repository IDs")
    for repo in repos:
        path=ROOT/repo.get("path","")
        for rel in ("README.md","pyproject.toml","tests"):
            target=path/rel
            if not target.exists(): errors.append(f"{repo.get('repository_id')}: required project path missing: {rel}")
        if repo.get("task_count")!=10: errors.append(f"{repo.get('repository_id')}: declared task_count must be ten")
    if len(repos)>60: errors.append("repository inventory exceeds 60")
    print(f"repositories: {len(repos)}/60; errors: {len(errors)}")
    for error in errors: print(error)
    return int(bool(errors))
if __name__=="__main__": raise SystemExit(main())
