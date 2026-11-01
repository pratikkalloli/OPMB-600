#!/usr/bin/env python3
"""Full Team B allocation audit; reports structural evidence and known quality limits."""
from __future__ import annotations
import ast,csv,hashlib,json,re,sys
from collections import Counter
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[4]; TEAM=Path(__file__).resolve().parent

class Shape(ast.NodeTransformer):
    """Normalize names and literal values to measure repeated code structure."""
    def visit_Name(self,n): n.id='IDENT'; return n
    def visit_Attribute(self,n): self.generic_visit(n); n.attr='ATTR'; return n
    def visit_arg(self,n): n.arg='ARG'; return n
    def visit_FunctionDef(self,n): n.name='FUNCTION'; self.generic_visit(n); return n
    def visit_AsyncFunctionDef(self,n): n.name='FUNCTION'; self.generic_visit(n); return n
    def visit_ClassDef(self,n): n.name='CLASS'; self.generic_visit(n); return n
    def visit_Constant(self,n):
        n.value='STRING' if isinstance(n.value,str) else 0 if isinstance(n.value,(int,float)) else n.value
        return n

def main()->int:
    repos=json.loads((TEAM/'repository_contribution_manifest.json').read_text())['repositories']
    tasks=json.loads((TEAM/'task_contribution_manifest.json').read_text())['tasks']
    specs=json.loads((TEAM/'application_specs.json').read_text()); errors=[]; warnings=[]
    repo_schema=Draft202012Validator(json.loads((ROOT/'benchmark/schemas/repository.schema.json').read_text()))
    task_schema=Draft202012Validator(json.loads((ROOT/'benchmark/schemas/task.schema.json').read_text()))
    repo_ids=[x['repository_id'] for x in repos]; task_ids=[x['task_id'] for x in tasks]
    if repo_ids!=[f'REPO-{n:03d}' for n in range(241,421)]: errors.append('repository IDs are not exactly continuous REPO-241..420')
    if sorted(task_ids)!=[f'OPMB-{n:04d}' for n in range(2401,4201)]: errors.append('task IDs are not exactly continuous OPMB-2401..4200')
    if len(repos)!=180 or len(set(repo_ids))!=180: errors.append(f'repository record count/uniqueness issue: {len(repos)}')
    if len(tasks)!=1800 or len(set(task_ids))!=1800: errors.append(f'task record count/uniqueness issue: {len(tasks)}')
    byrepo={}
    for t in tasks: byrepo.setdefault(t['repository_id'],[]).append(t)
    shape_hashes=[]; task_count_errors=[]; mismatches=[]; domain_rows=[]
    generic_methods={'__init__','register','retrieve','approve','verify_approval','advance','_commit_domain_decision'}
    for r in repos:
        errs=list(repo_schema.iter_errors(r)); errors.extend(f"{r['repository_id']} schema: {e.message}" for e in errs)
        rid=r['repository_id']; app=ROOT/r['path']; own=byrepo.get(rid,[]); n=int(rid[-3:])
        expected=[f'OPMB-{n*10-9+i:04d}' for i in range(10)]
        if sorted(t['task_id'] for t in own)!=expected: task_count_errors.append(rid)
        for rel in ('README.md','pyproject.toml','requirements.txt','src','migrated_reference','tests','tasks'):
            if not (app/rel).exists(): errors.append(f'{rid} missing {rel}')
        service=next(app.glob('src/*/service.py'),None)
        original_service_defs=set(); specialized=set()
        if service:
            raw=ast.parse(service.read_text(encoding='utf-8'))
            tree=Shape().visit(ast.parse(service.read_text(encoding='utf-8'))); shape_hashes.append(hashlib.sha256(ast.dump(tree,include_attributes=False).encode()).hexdigest())
            original_service_defs={x.name for x in ast.walk(raw) if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
            specialized=original_service_defs-generic_methods
        app_defs={}
        for p in app.glob('src/**/*.py'):
            try: app_defs[p.relative_to(app).as_posix()]={x.name for x in ast.walk(ast.parse(p.read_text(encoding='utf-8'))) if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
            except (SyntaxError,UnicodeError) as e: errors.append(f"{rid} source parse: {e}")
        ref=ROOT/'benchmark'/'repositories'/rid/'migrated_reference'
        ref_defs={x.name for p in ref.rglob('*.py') for x in ast.walk(ast.parse(p.read_text(encoding='utf-8'))) if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))} if ref.exists() else set()
        suite_calls={'original':set(),'pqc':set()}; suite_test_functions={'original':0,'pqc':0}
        for kind, key in (('original','original_tests'),('pqc','migration_tests')):
            paths={rel for t in own for rel in t.get(key,[])}
            for rel in paths:
                p=app/rel
                if not p.is_file(): continue
                try: tree=ast.parse(p.read_text(encoding='utf-8'))
                except (SyntaxError,UnicodeError): continue
                suite_calls[kind]|={n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)}
                suite_test_functions[kind]+=sum(1 for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test_'))
        if len(list((app/'tasks').glob('OPMB-*')))!=10: task_count_errors.append(rid+' task-directory-count')
        domain_methods=sorted(m for m in specialized if m not in {'main','cli','run','build_app'})
        method_evidence={m:{'original_source':m in original_service_defs,'pqc_reference':m in ref_defs,'original_tests_call':m in suite_calls['original'],'pqc_tests_call':m in suite_calls['pqc'],'business_guard_present':False} for m in domain_methods}
        for m in domain_methods:
            fn=next((n for n in ast.walk(ast.parse(service.read_text(encoding='utf-8'))) if isinstance(n,ast.FunctionDef) and n.name==m),None) if service else None
            if fn:
                body=ast.dump(fn,include_attributes=False)
                method_evidence[m]['business_guard_present']=('verify_approval' in body and '_commit_domain_decision' in body and 'Raise(' in body)
        workflow_ready=(len(domain_methods)==1 and all(x['original_source'] and x['pqc_reference'] and x['original_tests_call'] and x['pqc_tests_call'] and x['business_guard_present'] for x in method_evidence.values()) and suite_test_functions['original']>=8 and suite_test_functions['pqc']>=8)
        domain_rows.append({'repository_id':rid,'name':r['name'],'domain_methods':domain_methods,'method_evidence':method_evidence,'original_test_functions':suite_test_functions['original'],'pqc_test_functions':suite_test_functions['pqc'],'domain_specificity_status':'passes_internal_evidence_check' if workflow_ready else 'requires_remediation','review_note':'Automated evidence check only; not independent acceptance review.'})
        for t in own:
            errors.extend(f"{t['task_id']} schema: {e.message}" for e in task_schema.iter_errors(t))
            td=ROOT/t['task_path']/'task.json'
            if not td.is_file() or json.loads(td.read_text())!=t: errors.append(f"{t['task_id']} task.json missing or differs from manifest")
            defs=set()
            for rel in t['source_files']:
                if rel.startswith('migrated_reference/'):
                    if not (app/rel).is_file(): errors.append(f"{t['task_id']} source absent/invalid: {rel}")
                    else: defs|=ref_defs
                    continue
                if rel not in app_defs: errors.append(f"{t['task_id']} source absent/invalid: {rel}"); continue
                defs|=app_defs[rel]
            for fn in t['function_names']:
                if fn not in defs: errors.append(f"{t['task_id']} source function absent: {fn}")
            for rel in t['original_tests']+t.get('migration_tests',[]):
                if not (app/rel).is_file(): errors.append(f"{t['task_id']} test absent: {rel}")
            ref=ROOT/t.get('reference_path','')
            if not ref.is_dir(): errors.append(f"{t['task_id']} PQC reference absent")
            else:
                for fn in t['function_names']:
                    if fn not in ref_defs: errors.append(f"{t['task_id']} reference function absent: {fn}")
            ev=ROOT/'reports'/'evidence'/rid
            for ef in ('test-results.json','crypto-verification.json','post-migration-scan.json'):
                if not (ev/ef).is_file(): errors.append(f"{t['task_id']} evidence missing {ef}")
            if t['validation_status']!='candidate': warnings.append(f"{t['task_id']} non-candidate status: {t['validation_status']}")
    if task_count_errors: errors.append('task cardinality/mapping errors: '+', '.join(task_count_errors[:20]))
    baseline_repos=json.loads((ROOT/'benchmark/manifests/repositories.json').read_text()).get('repositories',[])
    baseline_tasks=json.loads((ROOT/'benchmark/manifests/tasks.json').read_text()).get('tasks',[])
    if set(repo_ids)&{x['repository_id'] for x in baseline_repos}: errors.append('repository ID collision with baseline')
    if set(task_ids)&{x['task_id'] for x in baseline_tasks}: errors.append('task ID collision with baseline')
    batch_results=[]
    for b in range(1,19):
        q=TEAM/f'batch-{b:02d}'; v=json.loads((q/'validation.json').read_text()); tr=json.loads((q/'test-results.json').read_text())
        batch_results.append(tr)
        if v['status']!='passed' or v['repositories']!=10 or v['tasks']!=100: errors.append(f'batch {b} structural validation not passed')
        expected_tests=sum(y['tests'] or 0 for x in tr['applications'] for y in x['suites'])
        expected_passed=sum(y['passed'] or 0 for x in tr['applications'] for y in x['suites'])
        expected_failed=sum(y['failed'] or 0 for x in tr['applications'] for y in x['suites'])
        expected_skipped=sum(y['skipped'] or 0 for x in tr['applications'] for y in x['suites'])
        if tr['total_suites']!=20 or tr['total_tests']!=expected_tests or tr['total_passed']!=expected_passed or tr['total_failed']!=expected_failed or tr['total_skipped']!=expected_skipped or expected_failed or expected_skipped: errors.append(f'batch {b} test summary inconsistent')
        for a in tr['applications']:
            test_ev=json.loads((ROOT/'reports'/'evidence'/a['repository_id']/'test-results.json').read_text())
            actual=sum(y['tests'] or 0 for y in a['suites']); passed=sum(y['passed'] or 0 for y in a['suites']); failed=sum(y['failed'] or 0 for y in a['suites']); skipped=sum(y['skipped'] or 0 for y in a['suites'])
            if test_ev['total_tests']!=actual or test_ev['passed']!=passed or test_ev['failed']!=failed or test_ev['skipped']!=skipped or failed or skipped: errors.append(f"{a['repository_id']} evidence test totals mismatch")
    names=[r['name'].casefold() for r in repos]
    if len(set(names))!=180: errors.append('duplicate application names')
    if len({t['migration_objective'] for t in tasks})!=1800: errors.append('duplicate task objectives')
    unique_service_shapes=len(set(shape_hashes))
    if unique_service_shapes < len(repos): warnings.append(f'Only {unique_service_shapes} normalized service-code shape(s) across {len(repos)} applications; domain-specific workflow behavior requires substantive independent review.')
    # Titles for existing REPO-001..060 are the available baseline concept catalogue.
    oldtitles=set()
    for f in (ROOT/'benchmark'/'repositories').glob('REPO-*/README.md'):
        try: number=int(f.parent.name[-3:])
        except ValueError: continue
        if number<241:
            m=re.search(r'^#\s+(.+)',f.read_text(encoding='utf-8'),re.M)
            if m: oldtitles.add(m.group(1).strip().casefold())
    title_overlap=[r['repository_id'] for r in repos if r['name'].casefold() in oldtitles]
    if title_overlap: errors.append('application title overlaps: '+','.join(title_overlap))
    secret=re.compile(r'BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}')
    secret_hits=[]; artifact_hits=[]
    for n in range(241,421):
        for folder in (ROOT/'benchmark'/'repositories'/f'REPO-{n:03d}',ROOT/'reports'/'evidence'/f'REPO-{n:03d}'):
            for p in folder.rglob('*'):
                if p.is_file():
                    if p.name.lower() in {'.env','private.key','database.sqlite','test.db'} or '__pycache__' in p.parts or '.pytest_cache' in p.parts: artifact_hits.append(str(p.relative_to(ROOT)))
                    if p.suffix.lower() in {'.py','.json','.md','.log','.toml','.txt','.xml'} and secret.search(p.read_text(encoding='utf-8',errors='ignore')): secret_hits.append(str(p.relative_to(ROOT)))
    if secret_hits: errors.append(f'secret patterns: {len(secret_hits)}')
    if artifact_hits: errors.append(f'local-only artifacts: {len(artifact_hits)}')
    remediated=sum(x['domain_specificity_status']=='passes_internal_evidence_check' for x in domain_rows)
    (TEAM/'domain_specificity_audit.json').write_text(json.dumps({'applications_reviewed':len(domain_rows),'applications_passing_internal_evidence_check':remediated,'applications_requiring_remediation':len(domain_rows)-remediated,'criteria':'One non-generic service operation exists in original and PQC code; both separate test suites call it; method verifies signed approval, enforces business guards, and persists a domain decision; each suite includes at least eight tests. This is not independent acceptance review.','applications':domain_rows},indent=2)+'\n',encoding='utf-8')
    summary={'repositories':len(repos),'tasks':len(tasks),'repository_ids_continuous':not any('repository IDs' in e for e in errors),'task_ids_continuous':not any('task IDs' in e for e in errors),'schema_dialect':'Draft 2020-12','pytest_suites':sum(x['total_suites'] for x in batch_results),'tests':sum(x['total_tests'] for x in batch_results),'passed':sum(x['total_passed'] for x in batch_results),'failed':sum(x['total_failed'] for x in batch_results),'skipped':sum(x['total_skipped'] for x in batch_results),'exact_title_overlaps_with_existing':len(title_overlap),'unique_normalized_service_shapes':unique_service_shapes,'domain_specificity_review':'partial' if remediated<len(repos) else 'passes internal evidence check; requires independent review','domain_specificity_apps_passed':remediated,'domain_specificity_apps_remaining':len(repos)-remediated,'secret_pattern_hits':len(secret_hits),'local_artifact_hits':len(artifact_hits),'errors':errors,'warnings':warnings,'structural_status':'passed' if not errors else 'failed','status':'incomplete' if not errors and remediated<len(repos) else ('passed' if not errors else 'failed')}
    (TEAM/'full_allocation_audit.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2)); return int(bool(errors))
if __name__=='__main__': raise SystemExit(main())
