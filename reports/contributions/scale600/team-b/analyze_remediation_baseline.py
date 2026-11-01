#!/usr/bin/env python3
"""Inventory domain behavior before Team B application remediation."""
from __future__ import annotations
import ast,csv,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]; TEAM=Path(__file__).resolve().parent

class Normalize(ast.NodeTransformer):
    def visit_Name(self,n): n.id='IDENT'; return n
    def visit_Attribute(self,n): self.generic_visit(n); n.attr='ATTR'; return n
    def visit_arg(self,n): n.arg='ARG'; return n
    def visit_FunctionDef(self,n): n.name='FUNCTION'; self.generic_visit(n); return n
    def visit_ClassDef(self,n): n.name='CLASS'; self.generic_visit(n); return n
    def visit_Constant(self,n): n.value='STRING' if isinstance(n.value,str) else (0 if isinstance(n.value,(int,float)) else n.value); return n
    def visit_ImportFrom(self,n): n.module='MODULE'; self.generic_visit(n); return n
    def visit_alias(self,n): n.name='MODULE'; n.asname=None; return n

def main()->None:
    specs=json.loads((TEAM/'application_specs.json').read_text(encoding='utf-8')); repo_rows=[]; svc_hash=Counter(); test_hash=Counter(); domain_hash=Counter(); methodsets=Counter(); testnames=Counter(); rule_kinds=Counter(); workflow_methods=Counter()
    for s in specs:
        app=ROOT/'benchmark'/'repositories'/s['repository_id']; service=next(app.glob('src/*/service.py')); domain=next(app.glob('src/*/domain.py')); testfiles=list((app/'tests').glob('test_*.py'))
        st=ast.parse(service.read_text(encoding='utf-8')); dt=ast.parse(domain.read_text(encoding='utf-8'))
        service_shape=hashlib.sha256(ast.dump(Normalize().visit(ast.parse(service.read_text(encoding='utf-8'))),include_attributes=False).encode()).hexdigest(); svc_hash[service_shape]+=1
        domain_shape=hashlib.sha256(ast.dump(Normalize().visit(dt),include_attributes=False).encode()).hexdigest(); domain_hash[domain_shape]+=1
        methods=sorted(n.name for n in ast.walk(st) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))); methodsets[','.join(methods)]+=1
        testtrees=[ast.parse(f.read_text(encoding='utf-8')) for f in testfiles]
        names=sorted(n.name for tree in testtrees for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)))
        testnames[','.join(names)]+=1
        tshape='|'.join(ast.dump(Normalize().visit(tree),include_attributes=False) for tree in testtrees); test_hash[hashlib.sha256(tshape.encode()).hexdigest()]+=1
        rule_kinds[s['rule_kind']]+=1
        # Domain-specific behavior is present only when service methods express a real app operation beyond the shared record API.
        generic={'__init__','register','retrieve','approve','verify_approval','advance'}
        specialized=sorted(set(methods)-generic)
        workflow_methods.update(specialized)
        repo_rows.append({'repository_id':s['repository_id'],'name':s['name'],'domain':s['domain_group'],'purpose':s['purpose'],'service_methods':';'.join(methods),'specialized_service_methods':';'.join(specialized),'domain_validator_functions':';'.join(sorted(n.name for n in ast.walk(dt) if isinstance(n,ast.FunctionDef))),'test_functions':';'.join(names),'rule_kind':s['rule_kind'],'status':'requires remediation' if not specialized else 'needs review'})
    report={'applications_reviewed':len(specs),'service_shapes':len(svc_hash),'service_shape_distribution':dict(svc_hash),'service_method_sets':dict(methodsets),'applications_with_only_generic_record_service':sum(1 for r in repo_rows if not r['specialized_service_methods']),'applications_with_specialized_service_methods':sum(1 for r in repo_rows if r['specialized_service_methods']),'domain_module_shapes':len(domain_hash),'domain_rule_kind_distribution':dict(rule_kinds),'test_shapes':len(test_hash),'test_function_sets':dict(testnames),'shared_specialized_method_names':dict(workflow_methods),'assessment':'Existing service and test behavior is generic; domain purpose is largely represented by fields, rule kind, and lifecycle configuration. Each app requires workflow-level review; no app is presumed adequate solely because names or rule values differ.'}
    (TEAM/'remediation_baseline.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    with (TEAM/'remediation_inventory.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(repo_rows[0])); w.writeheader(); w.writerows(repo_rows)
    (TEAM/'remediation_baseline.md').write_text(f"""# Remediation inventory — current checkpoint

Inspected {len(specs)} assigned applications from the actual service, domain, test and concept files.

- Normalized service implementation shapes: {len(svc_hash)}.
- Applications whose service exposes only the shared `register` / `retrieve` / `approve` / `verify_approval` / `advance` record API: {report['applications_with_only_generic_record_service']}.
- Applications already exposing specialized service operations: {report['applications_with_specialized_service_methods']}.
- Normalized test module shapes: {len(test_hash)}.
- Domain validator modules differ in rule expression/configuration, but this alone does not establish the README-described workflow.
- All assigned IDs, concepts, service methods, domain functions, and test function names are enumerated in `remediation_inventory.csv`.

This is a current inventory, not a final acceptance audit. No application is considered domain-specific solely because its title, field, rule value, enum, or lifecycle label differs. The separately maintained domain audit records workflow tests and specialized service behavior.
""",encoding='utf-8',newline='\n')
    print(json.dumps({k:report[k] for k in ('applications_reviewed','service_shapes','applications_with_only_generic_record_service','applications_with_specialized_service_methods','domain_module_shapes','test_shapes','domain_rule_kind_distribution')},indent=2))
if __name__=='__main__': main()
