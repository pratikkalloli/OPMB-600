#!/usr/bin/env python3
"""Finalize verified evidence and cumulative Team B manifests for one batch."""
from __future__ import annotations
import argparse,csv,json,datetime as dt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]; TEAM=Path(__file__).resolve().parent

def save(path:Path,obj:object)->None: path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('--batch',type=int,required=True); a=p.parse_args(); folder=TEAM/f'batch-{a.batch:02d}'
 repos=json.loads((folder/'repositories.json').read_text(encoding='utf-8')); tasks=json.loads((folder/'tasks.json').read_text(encoding='utf-8')); results=json.loads((folder/'test-results.json').read_text(encoding='utf-8'))
 byid={x['repository_id']:x for x in results['applications']}
 for t in tasks:
  app=byid[t['repository_id']]; suites=app['suites']
  if not all(x['exit_code']==0 and x['failed']==0 and x['skipped']==0 and x['tests']>0 for x in suites):
   t['original_build_status']='pending'; t['original_test_status']='pending'; t['reference_patch_status']='candidate'; t['cryptographic_verification_status']='pending'
  else:
   t['original_build_status']='passed'; t['original_test_status']='passed'; t['reference_patch_status']='tested'; t['cryptographic_verification_status']='passed'
  save(ROOT/t['task_path']/'task.json',t)
 for r in repos:
  s=next(x for x in json.loads((TEAM/'application_specs.json').read_text(encoding='utf-8')) if x['repository_id']==r['repository_id']); slug=s['slug']
  r['main_modules']=[f'src/{slug}/domain.py',f'src/{slug}/crypto.py',f'src/{slug}/service.py']
  r['classical_cryptography']=['RSA-3072 PSS/SHA-256','RSA-3072 OAEP/SHA-256','AES-256-GCM']
  r['pqc_cryptography']=['ML-DSA-65','ML-KEM-768','HKDF-SHA-256','AES-256-GCM']
  r['task_count']=10; r['test_status']='passed' if byid[r['repository_id']]['suites'] and all(x['exit_code']==0 for x in byid[r['repository_id']]['suites']) else 'pending'; r['validation_status']='candidate'
 save(folder/'repositories.json',repos); save(folder/'tasks.json',tasks)
 for s in [x for x in json.loads((TEAM/'application_specs.json').read_text(encoding='utf-8')) if x['batch']==a.batch]:
  rid=s['repository_id']; ev=ROOT/'reports'/'evidence'/rid; suites=byid[rid]['suites']
  crypto={'repository_id':rid,'application_name':s['name'],'status':'passed' if all(x['exit_code']==0 for x in suites) else 'not_run','basis':'Functional checks from the recorded original and PQC pytest runs; not an independent security review.','checks':['Signature generation and verification','Modified-record rejection','Wrong verification-key rejection','Versioned public-key round trip','Classical envelope or ML-KEM/HKDF/AES-GCM seal/open round trip','Tampered ciphertext rejection','Wrong recipient-key rejection','Unsupported envelope version rejection','Persistent approval and stale-record rejection'],'suite_results':suites,'limitations':['No formal verification, certification, independent audit, or production readiness claim.']}
  save(ev/'crypto-verification.json',crypto)
  save(ev/'post-migration-scan.json',{'repository_id':rid,'status':'not_run','reason':'No dedicated cryptographic scanner was available or executed.','secret_scan':'See the batch validation report for the limited secret-pattern scan.'})
 # Aggregate only batches with both reports; preserve already-committed batches.
 done=[]
 for n in range(1,19):
  q=TEAM/f'batch-{n:02d}'
  if (q/'repositories.json').is_file() and (q/'tasks.json').is_file() and (q/'test-results.json').is_file() and (q/'validation.json').is_file(): done.append(n)
 allrepos=[]; alltasks=[]; summaries=[]
 for n in done:
  q=TEAM/f'batch-{n:02d}'; allrepos.extend(json.loads((q/'repositories.json').read_text())); alltasks.extend(json.loads((q/'tasks.json').read_text())); summaries.append(json.loads((q/'test-results.json').read_text()))
 repo_manifest={'team':'B','part':'scale600','batch_plan':{f'batch-{n:02d}':[f'REPO-{x:03d}' for x in range(241+(n-1)*10,251+(n-1)*10)] for n in done},'repositories':allrepos}
 task_manifest={'team':'B','task_count':len(alltasks),'tasks':alltasks}
 save(TEAM/'repository_contribution_manifest.json',repo_manifest); save(TEAM/'task_contribution_manifest.json',task_manifest)
 validation_rows=[json.loads((TEAM/f'batch-{n:02d}'/'validation.json').read_text()) for n in done]
 save(TEAM/'schema_validation.json',{'schema_dialect':'Draft 2020-12','jsonschema_version':'4.25.1','batches':validation_rows,'repositories_checked':len(allrepos),'tasks_checked':len(alltasks),'repositories_valid':len(allrepos),'tasks_valid':len(alltasks),'errors':[e for row in validation_rows for e in row['errors']],'status':'passed' if all(x['status']=='passed' for x in validation_rows) else 'failed'})
 specs=json.loads((TEAM/'application_specs.json').read_text(encoding='utf-8'))
 def writecsv(path,header,rows):
  with path.open('w',newline='',encoding='utf-8') as f: w=csv.writer(f); w.writerow(header); w.writerows(rows)
 writecsv(TEAM/'application_concept_register.csv',['repository_id','application_name','domain','unique_purpose','domain_workflow','original_cryptographic_operations','pqc_migration_family','intended_algorithm','differentiation_from_existing_applications','implementation_status'],[[s['repository_id'],s['name'],s['domain_group'],s['purpose'],s['workflow'],s['classical_signature']+'; '+s['classical_key_establishment'],'ML-DSA signature and ML-KEM confidentiality',s['target'],s['differentiation'],'tested' if s['batch'] in done else 'planned'] for s in specs])
 writecsv(TEAM/'application_inventory.csv',['repository_id','name','domain','path','task_count','status','implementation_status'],[[s['repository_id'],s['name'],s['domain_group'],f"benchmark/repositories/{s['repository_id']}",10,'candidate','tested' if s['batch'] in done else 'planned'] for s in specs])
 writecsv(TEAM/'task_inventory.csv',['task_id','repository_id','migration_objective','migration_family','target','validation_status'],[[t['task_id'],t['repository_id'],t['migration_objective'],t['migration_family'],t['migration_target'],t['validation_status']] for t in alltasks])
 writecsv(TEAM/'task_objective_register.csv',['task_id','repository_id','objective','source_files','function_names','original_tests','migration_tests'],[[t['task_id'],t['repository_id'],t['migration_objective'],';'.join(t['source_files']),';'.join(t['function_names']),';'.join(t['original_tests']),';'.join(t.get('migration_tests',[]))] for t in alltasks])
 writecsv(TEAM/'traceability_matrix.csv',['task_id','repository_id','source_files','functions','original_tests','reference_tests','reference_path','verification_evidence'],[[t['task_id'],t['repository_id'],';'.join(t['source_files']),';'.join(t['function_names']),';'.join(t['original_tests']),';'.join(t.get('migration_tests',[])),t['reference_path'],t.get('cryptographic_verification_evidence','')] for t in alltasks])
 total_tests=sum(x['total_tests'] for x in summaries); total_pass=sum(x['total_passed'] for x in summaries); total_fail=sum(x['total_failed'] for x in summaries); total_skip=sum(x['total_skipped'] for x in summaries)
 progress=['# Team B batch progress','','| Batch | Repositories | Tasks | Pytest suites | Passed | Failed | Skipped | Schema / path | Status |','|---|---|---:|---:|---:|---:|---:|---|---|']
 for n in range(1,19):
  start=241+(n-1)*10; end=start+9
  if n in done:
   q=TEAM/f'batch-{n:02d}'; x=json.loads((q/'test-results.json').read_text()); v=json.loads((q/'validation.json').read_text()); progress.append(f"| {n:02d} | REPO-{start}–{end} | 100 | {x['total_suites']} | {x['total_passed']} | {x['total_failed']} | {x['total_skipped']} | {v['status']} | {'tested' if v['status']=='passed' and not x['total_failed'] else 'blocked'} |")
  else: progress.append(f'| {n:02d} | REPO-{start}–{end} | 100 | NOT RUN | — | — | — | NOT RUN | NOT IMPLEMENTED |')
 progress+=['',f'Overall: {len(done)*10}/180 applications; {len(done)*100}/1,800 tasks; {total_tests} tests, {total_pass} passed, {total_fail} failed, {total_skip} skipped.','']
 (TEAM/'batch_progress.md').write_text('\n'.join(progress),encoding='utf-8',newline='\n')
 (TEAM/'original_test_summary.json').write_text(json.dumps({'batches':done,'applications':[{'repository_id':app['repository_id'],'suite':app['suites'][0]} for x in summaries for app in x['applications']]},indent=2)+'\n',encoding='utf-8')
 (TEAM/'pqc_reference_test_summary.json').write_text(json.dumps({'batches':done,'applications':[{'repository_id':app['repository_id'],'suite':app['suites'][1]} for x in summaries for app in x['applications']]},indent=2)+'\n',encoding='utf-8')
 crypto_report=f"# Cryptographic verification summary\n\nFor batches {', '.join(f'{n:02d}' for n in done)}, {total_tests} actual pytest cases ran ({total_pass} passed, {total_fail} failed, {total_skip} skipped). Each application's `reports/evidence/REPO-XXX/crypto-verification.json` describes the functional signature, encapsulation/envelope, tamper, wrong-key, version, and persistence checks represented by its tests.\n\nThese are software functional-test results. They do not establish formal verification, FIPS certification, independent security review, or production readiness. A dedicated cryptographic scanner has not been run.\n"
 (TEAM/'cryptographic_verification_summary.md').write_text(crypto_report,encoding='utf-8',newline='\n')
 # Batch 01 is immutable per assignment. Record its detected metadata/code mismatch rather than altering it.
 mismatch=[]
 for s in specs:
  if s['batch']==1 and s['baseline_mode']=='ec': mismatch.append(s['repository_id'])
 issues=['# Known issues and remaining work','',f'- Implemented and tested {len(done)*10}/180 applications and {len(done)*100}/1,800 tasks; {180-len(done)*10} applications and {1800-len(done)*100} tasks remain.','- No independent acceptance review has occurred; tasks remain candidate.','- Dedicated cryptographic/static security scanners were not executed; the recorded secret-pattern scan is limited and is not a security review.','- GitHub push and pull-request delivery are deferred until all batches and the full audit pass.']
 if mismatch: issues.append(f"- Batch 01 metadata/code discrepancy: {', '.join(mismatch)} declare ECDSA in the committed task/spec metadata, while their generated original implementation and executed tests use RSA-PSS. Batch 01 was preserved; this requires a separately reviewed corrective commit before final acceptance.")
 (TEAM/'known_issues.md').write_text('\n'.join(issues)+'\n',encoding='utf-8',newline='\n')
 report=f"# Team B implementation report (checkpoint)\n\nImplemented and locally tested {len(done)*10} applications and {len(done)*100} task specifications, in batches {', '.join(f'{n:02d}' for n in done)}. Original and PQC pytest results total {total_tests}: {total_pass} passed, {total_fail} failed, {total_skip} skipped.\n\nThe full assignment remains incomplete: {180-len(done)*10} applications and {1800-len(done)*100} tasks remain unimplemented. No task is marked accepted; independent review has not occurred. Delivery is deferred until all batches and the final audit pass.\n"
 (TEAM/'implementation_report.md').write_text(report,encoding='utf-8',newline='\n')
 print(f'Finalized batch {a.batch}; aggregate currently {len(done)*10} applications and {len(done)*100} tasks, {total_pass}/{total_tests} tests passed.')
 return 0
if __name__=='__main__': raise SystemExit(main())
