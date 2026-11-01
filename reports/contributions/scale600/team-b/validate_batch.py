#!/usr/bin/env python3
"""Validate one local Team B scale600 batch without touching shared manifests."""
from __future__ import annotations
import argparse, ast, json, re, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[4]
TEAM=Path(__file__).resolve().parent
SECRET=re.compile(r'BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}')

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--batch',type=int,required=True); a=p.parse_args()
    folder=TEAM/f'batch-{a.batch:02d}'
    repos=json.loads((folder/'repositories.json').read_text(encoding='utf-8'))
    tasks=json.loads((folder/'tasks.json').read_text(encoding='utf-8'))
    rs=Draft202012Validator(json.loads((ROOT/'benchmark/schemas/repository.schema.json').read_text()))
    ts=Draft202012Validator(json.loads((ROOT/'benchmark/schemas/task.schema.json').read_text()))
    errors=[]
    for r in repos: errors.extend(f"{r.get('repository_id')}: {e.message}" for e in rs.iter_errors(r))
    for t in tasks: errors.extend(f"{t.get('task_id')}: {e.message}" for e in ts.iter_errors(t))
    if len(repos)!=10 or len(tasks)!=100: errors.append('batch must contain exactly ten applications and 100 tasks')
    if len({r['repository_id'] for r in repos})!=len(repos): errors.append('duplicate repository ID')
    if len({t['task_id'] for t in tasks})!=len(tasks): errors.append('duplicate task ID')
    if len({t['migration_objective'] for t in tasks})!=len(tasks): errors.append('duplicate migration objective')
    for r in repos:
        app=ROOT/r['path']; own=[t for t in tasks if t['repository_id']==r['repository_id']]
        if len(own)!=10: errors.append(f"{r['repository_id']}: expected ten tasks")
        for t in own:
            source_defs=set()
            for rel in t['source_files']:
                path=app/rel
                if not path.is_file(): errors.append(f"{t['task_id']}: source absent: {rel}"); continue
                try: source_defs|={n.name for n in ast.walk(ast.parse(path.read_text(encoding='utf-8'))) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
                except (SyntaxError,UnicodeError) as e: errors.append(f"{t['task_id']}: source parse error: {e}")
            for fn in t['function_names']:
                if fn not in source_defs: errors.append(f"{t['task_id']}: function absent from source files: {fn}")
            for rel in t['original_tests']+t.get('migration_tests',[]):
                if not (app/rel).is_file(): errors.append(f"{t['task_id']}: test file absent: {rel}")
            if not (ROOT/t['task_path']/'task.json').is_file(): errors.append(f"{t['task_id']}: task directory/file absent")
            if not (ROOT/t['reference_path']).is_dir(): errors.append(f"{t['task_id']}: PQC reference absent")
        for tree in ('src','migrated_reference','tests'):
            for path in (app/tree).rglob('*'):
                if path.is_file() and path.suffix in {'.py','.json','.md'} and SECRET.search(path.read_text(encoding='utf-8',errors='replace')):
                    errors.append(f'{r["repository_id"]}: secret-like pattern in {path.relative_to(ROOT)}')
    summary={'batch':a.batch,'repositories':len(repos),'tasks':len(tasks),'schema_dialect':'Draft 2020-12','secret_pattern_scan':'passed' if not any('secret-like' in e for e in errors) else 'failed','errors':errors,'status':'passed' if not errors else 'failed'}
    (folder/'validation.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2)); return int(bool(errors))
if __name__=='__main__': raise SystemExit(main())
