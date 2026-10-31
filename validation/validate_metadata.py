"""Validate task and repository manifests against JSON schemas."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT = Path(__file__).resolve().parents[1]
def main() -> int:
    errors=[]
    schema_dir=ROOT/"benchmark/schemas"
    for name,manifest,collection in [("repository","benchmark/manifests/repositories.json","repositories"),("task","benchmark/manifests/tasks.json","tasks")]:
        schema=json.loads((schema_dir/f"{name}.schema.json").read_text(encoding="utf-8"))
        data=json.loads((ROOT/manifest).read_text(encoding="utf-8"))
        for i,item in enumerate(data.get(collection, [])):
            for err in Draft202012Validator(schema).iter_errors(item): errors.append(f"{manifest}[{i}]: {err.message}")
    print("metadata: "+("ok" if not errors else f"{len(errors)} schema error(s)"))
    for e in errors: print(e)
    return bool(errors)
if __name__=="__main__": raise SystemExit(main())
