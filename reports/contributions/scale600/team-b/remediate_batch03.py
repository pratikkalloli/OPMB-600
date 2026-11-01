#!/usr/bin/env python3
"""Add distinct manufacturing-control workflows for REPO-261..270."""
from __future__ import annotations
import ast,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; TEAM=Path(__file__).resolve().parent
W={
261:("close_machine_guard_findings", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('guard inspection must be reviewed before restart clearance')
        if not isinstance(findings,list) or not findings: raise ValueError('inspection must enumerate guard findings')
        critical=[f for f in findings if not isinstance(f,dict) or f.get('class')=='safety_critical']
        if any(not isinstance(f,dict) or f.get('closed') is not True or not f.get('closure_evidence') for f in critical): raise ValueError('every safety-critical guard finding needs closure evidence')
        if not self.verify_approval(record_id,safety_public): raise PermissionError('restart inspection is missing a valid safety signature')
        return self._commit_domain_decision(record,'released','machine_guard_restart_cleared',{'workcell_id':record['workcell_id'],'finding_count':len(findings),'critical_closed':len(critical)})""", "findings=[{'class':'safety_critical','closed':True,'closure_evidence':'CHK-261'}]", "findings=[{'class':'safety_critical','closed':False,'closure_evidence':''}]"),
262:("release_process_consumable", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('consumable shelf-life record must be reviewed before issue')
        if any(type(v) is not int for v in (opened_epoch,expiry_epoch,now_epoch,max_open_seconds)): raise ValueError('shelf-life timestamps and limit must be integer epochs')
        if opened_epoch<0 or expiry_epoch<=opened_epoch or max_open_seconds<=0: raise ValueError('invalid consumable shelf-life interval')
        if now_epoch<opened_epoch or now_epoch>=expiry_epoch or now_epoch-opened_epoch>=max_open_seconds: raise ValueError('consumable lot or opened container is expired')
        if lot_revision!=record['revision_epoch']: raise ValueError('consumable label revision does not match the approved lot card')
        if not self.verify_approval(record_id,warehouse_public): raise PermissionError('consumable issue lacks authorized shelf-life signoff')
        return self._commit_domain_decision(record,'released','process_consumable_issued',{'workcell_id':record['workcell_id'],'lot_revision':lot_revision,'opened_epoch':opened_epoch,'expiry_epoch':expiry_epoch,'issued_at':now_epoch})""", "opened_epoch=100, expiry_epoch=1000, now_epoch=200, max_open_seconds=500, lot_revision=RECORD['revision_epoch']", "opened_epoch=100, expiry_epoch=1000, now_epoch=700, max_open_seconds=500, lot_revision=RECORD['revision_epoch']"),
263:("approve_gauge_repeatability_study", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('gauge study must be reviewed before approval')
        if not isinstance(samples,list) or len(samples)<2 or any(type(x) not in (int,float) for x in samples): raise ValueError('gauge study requires at least two numeric samples')
        if type(maximum_spread) not in (int,float) or maximum_spread<0 or max(samples)-min(samples)>maximum_spread: raise ValueError('measurement variation exceeds the approved study spread')
        if study_digest!=record['evidence_digest']: raise ValueError('study dataset digest differs from the controlled gauge record')
        if not self.verify_approval(record_id,metrology_public): raise PermissionError('metrology approval signature is invalid')
        return self._commit_domain_decision(record,'released','gauge_r_and_r_approved',{'workcell_id':record['workcell_id'],'sample_count':len(samples),'spread':max(samples)-min(samples),'study_digest':study_digest})""", "samples=[10.0,10.2,10.1], maximum_spread=0.5, study_digest=RECORD['evidence_digest']", "samples=[10.0,11.0,10.1], maximum_spread=0.5, study_digest=RECORD['evidence_digest']"),
264:("complete_work_order_traveler", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('traveler must be reviewed before final station signoff')
        if not isinstance(required_operations,list) or not required_operations or len(set(required_operations))!=len(required_operations): raise ValueError('work order route must have unique required operations')
        if not isinstance(station_signoffs,dict) or not set(required_operations).issubset(station_signoffs): raise ValueError('traveler is missing one or more station signoffs')
        if any(not isinstance(station_signoffs[o],str) or not station_signoffs[o].strip() for o in required_operations): raise ValueError('station signoffs must identify qualified operators')
        if authorization_code!=record['authorization_code']: raise PermissionError('traveler is scoped to a different work order authorization')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('final traveler signoff is invalid')
        return self._commit_domain_decision(record,'released','work_order_traveler_completed',{'workcell_id':record['workcell_id'],'operations':required_operations,'station_signoffs':station_signoffs,'authorization_code':authorization_code})""", "required_operations=['cut','form','inspect'], station_signoffs={'cut':'op-a','form':'op-b','inspect':'op-c'}, authorization_code=RECORD['authorization_code']", "required_operations=['cut','form','inspect'], station_signoffs={'cut':'op-a','form':'op-b'}, authorization_code=RECORD['authorization_code']"),
265:("release_contained_quality_hold", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('quality hold must be reviewed after containment')
        if not isinstance(affected_lots,list) or not affected_lots or len(set(affected_lots))!=len(affected_lots): raise ValueError('containment scope must list unique affected lots')
        if not isinstance(recheck_measurements,list) or not recheck_measurements: raise ValueError('hold release requires documented reinspection measurements')
        if type(lower_limit) not in (int,float) or type(upper_limit) not in (int,float) or lower_limit>upper_limit: raise ValueError('reinspection acceptance range is invalid')
        if any(type(x) not in (int,float) or not lower_limit<=x<=upper_limit for x in recheck_measurements): raise ValueError('one or more reinspection results remain outside release limits')
        if not self.verify_approval(record_id,quality_manager_public): raise PermissionError('quality manager release authorization is invalid')
        return self._commit_domain_decision(record,'released','quality_hold_released',{'affected_lots':affected_lots,'measurements':recheck_measurements,'acceptance_range':[lower_limit,upper_limit]})""", "affected_lots=['LOT-265-A'], recheck_measurements=[5,6], lower_limit=0, upper_limit=10, quality_manager_public=signer.public_key()", "affected_lots=['LOT-265-A'], recheck_measurements=[5,11], lower_limit=0, upper_limit=10, quality_manager_public=signer.public_key()"),
266:("approve_spare_part_fit", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('replacement part requires compatibility review')
        if machine_model not in set(approved_models): raise PermissionError('part is not approved for the installed machine model')
        if machine_revision not in set(compatible_revisions): raise ValueError('part compatibility does not cover this machine revision')
        if safety_class not in set(approved_safety_classes): raise PermissionError('replacement part safety class is not approved')
        if record['event_count']<1: raise ValueError('compatibility record must include at least one engineering review event')
        if not self.verify_approval(record_id,engineering_public): raise PermissionError('engineering compatibility approval is invalid')
        return self._commit_domain_decision(record,'released','spare_part_fit_approved',{'workcell_id':record['workcell_id'],'machine_model':machine_model,'machine_revision':machine_revision,'safety_class':safety_class})""", "machine_model='MX-266', approved_models={'MX-266'}, machine_revision='C', compatible_revisions={'B','C'}, safety_class='S2', approved_safety_classes={'S2'}", "machine_model='MX-266', approved_models={'MX-266'}, machine_revision='D', compatible_revisions={'B','C'}, safety_class='S2', approved_safety_classes={'S2'}"),
267:("release_vessel_after_cip", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('clean-in-place cycle must be reviewed before vessel reuse')
        required=['pre_rinse','wash','post_rinse','sanitize']
        if not isinstance(phases,list) or [p.get('name') for p in phases if isinstance(p,dict)]!=required: raise ValueError('CIP phases must be completed in validated process order')
        if any(type(p.get('duration_seconds')) is not int or p['duration_seconds']<minimum_duration for p in phases): raise ValueError('a CIP phase did not meet its minimum validated duration')
        if any(p.get('result')!='pass' for p in phases): raise ValueError('failed CIP phase blocks vessel reuse')
        if not next_lot or not next_lot.strip(): raise ValueError('next production lot must be assigned before CIP release')
        if not self.verify_approval(record_id,sanitation_public): raise PermissionError('sanitation release signature is invalid')
        return self._commit_domain_decision(record,'released','cip_vessel_released',{'vessel_id':record['workcell_id'],'phase_count':len(phases),'next_lot':next_lot})""", "phases=[{'name':n,'duration_seconds':60,'result':'pass'} for n in ['pre_rinse','wash','post_rinse','sanitize']], minimum_duration=30, next_lot='LOT-267-NEXT'", "phases=[{'name':n,'duration_seconds':60,'result':'pass'} for n in ['wash','pre_rinse','post_rinse','sanitize']], minimum_duration=30, next_lot='LOT-267-NEXT'"),
268:("approve_rework_route_completion", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('rework route must be reviewed before disposition')
        if not isinstance(permitted_steps,list) or not permitted_steps or len(set(permitted_steps))!=len(permitted_steps): raise ValueError('approved rework route must be ordered and unique')
        if not isinstance(completed_steps,list) or completed_steps!=permitted_steps: raise ValueError('unit has not completed the full authorized rework route in order')
        if not reinspection_passed: raise ValueError('reworked unit requires a passing independent reinspection')
        if type(route_revision) is not int or route_revision!=record['revision_epoch']: raise ValueError('rework route revision is stale')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('quality disposition signature is invalid')
        return self._commit_domain_decision(record,'released','rework_route_completed',{'workcell_id':record['workcell_id'],'route':permitted_steps,'route_revision':route_revision,'reinspection_passed':True})""", "permitted_steps=['remove_defect','replace_component','inspect'], completed_steps=['remove_defect','replace_component','inspect'], reinspection_passed=True, route_revision=RECORD['revision_epoch']", "permitted_steps=['remove_defect','replace_component','inspect'], completed_steps=['remove_defect','inspect'], reinspection_passed=True, route_revision=RECORD['revision_epoch']"),
269:("grant_operator_qualification", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('operator qualification evidence must be reviewed before grant')
        if type(now_epoch) is not int or type(expiry_epoch) is not int or expiry_epoch<=now_epoch: raise ValueError('qualification is expired or has an invalid validity interval')
        if not isinstance(requested_scope,set) or not requested_scope or not requested_scope.issubset(set(qualified_scope)): raise PermissionError('requested task scope exceeds demonstrated operator qualification')
        if training_digest!=record['evidence_digest']: raise ValueError('training evidence digest does not match the qualification record')
        if not self.verify_approval(record_id,qualification_public): raise PermissionError('qualification grant is missing authorized signoff')
        return self._commit_domain_decision(record,'released','operator_qualification_granted',{'workcell_id':record['workcell_id'],'scope':sorted(requested_scope),'expiry_epoch':expiry_epoch,'training_digest':training_digest})""", "now_epoch=100, expiry_epoch=200, requested_scope={'press_setup'}, qualified_scope={'press_setup','inspection'}, training_digest=RECORD['evidence_digest']", "now_epoch=100, expiry_epoch=200, requested_scope={'forklift'}, qualified_scope={'press_setup','inspection'}, training_digest=RECORD['evidence_digest']"),
270:("accept_retained_sample_custody", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('sample custody record must be reviewed before disposition')
        if not isinstance(custody_events,list) or not custody_events: raise ValueError('retained sample needs a custody event chain')
        if any(not isinstance(e,dict) or type(e.get('sequence')) is not int or not e.get('custodian') or not e.get('seal_id') for e in custody_events): raise ValueError('custody event is malformed or lacks seal attribution')
        if [e['sequence'] for e in custody_events]!=list(range(record['sequence'],record['sequence']+len(custody_events))): raise ValueError('sample custody chain has a sequence gap or replay')
        if disposition not in {'retain','archive','destroy'}: raise ValueError('unsupported retained-sample disposition')
        if disposition=='destroy' and not destruction_witness: raise PermissionError('sample destruction requires an independent witness')
        if not self.verify_approval(record_id,custodian_public): raise PermissionError('sample custody approval signature is invalid')
        return self._commit_domain_decision(record,'released','retained_sample_dispositioned',{'workcell_id':record['workcell_id'],'event_count':len(custody_events),'last_custodian':custody_events[-1]['custodian'],'disposition':disposition})""", "custody_events=[{'sequence':RECORD['sequence'],'custodian':'custodian-1','seal_id':'SEAL-270'}], disposition='retain', destruction_witness=None", "custody_events=[{'sequence':RECORD['sequence']+1,'custodian':'custodian-1','seal_id':'SEAL-270'}], disposition='retain', destruction_witness=None"),
}

def main():
 tasks=json.loads((TEAM/'batch-03'/'tasks.json').read_text(encoding='utf-8')); repos=json.loads((TEAM/'batch-03'/'repositories.json').read_text(encoding='utf-8')); specs={s['repository_id']:s for s in json.loads((TEAM/'application_specs.json').read_text(encoding='utf-8'))}
 for n,(method,body,good,bad) in W.items():
  rid=f'REPO-{n:03d}'; spec=specs[rid]; app=ROOT/'benchmark'/'repositories'/rid
  service=next(app.glob('src/*/service.py')); ref=next(app.glob('migrated_reference/*/service.py'))
  oc=next(x.name for x in ast.walk(ast.parse(service.read_text())) if isinstance(x,ast.ClassDef)); pc=next(x.name for x in ast.walk(ast.parse(ref.read_text())) if isinstance(x,ast.ClassDef))
  gkw={k.arg:ast.unparse(k.value) for k in ast.parse(f'f({good})',mode='eval').body.keywords}; bkw={k.arg:ast.unparse(k.value) for k in ast.parse(f'f({bad})',mode='eval').body.keywords}; pubs=sorted(set(re.findall(r'\b([a-z_]+_public)\b',body)))
  for p in pubs:gkw[p]='signer.public_key()'; bkw[p]='signer.public_key()'
  bkw={**gkw,**bkw}; gc=', '.join(f'{k}={v}' for k,v in gkw.items()); bc=', '.join(f'{k}={v}' for k,v in bkw.items())
  for path,cls in ((service,oc),(ref,pc)):
   src=path.read_text(encoding='utf-8'); mark=f'    def {method}('
   if mark not in src:
    unpack=''.join(f"        {k}=decision['{k}']\n" for k in gkw)
    src=src.rstrip()+f"\n\n    def {method}(self, record_id, **decision):\n        # Apply the {spec['name']} decision and preserve its signed evidence.\n"+unpack+body+'\n'
   if 'def _commit_domain_decision(' not in src:
    helper='''    def _commit_domain_decision(self, record, next_state, event_type, evidence):
        updated=transition_record(record,next_state)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS workflow_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, event_type TEXT NOT NULL, previous_state TEXT NOT NULL, next_state TEXT NOT NULL, evidence TEXT NOT NULL)")
            db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(updated,sort_keys=True),record['record_id']))
            db.execute("INSERT INTO workflow_events(record_id,event_type,previous_state,next_state,evidence) VALUES(?,?,?,?,?)",(record['record_id'],event_type,record['state'],next_state,json.dumps(evidence,sort_keys=True)))
        return updated

'''
    src=src.replace(mark,helper+mark,1)
   path.write_text(src,encoding='utf-8',newline='\n')
  for pqc,cls,pkg in ((False,oc,f'{spec["slug"]}.service'),(True,pc,f'migrated_reference.{spec["slug"]}_pqc.service')):
   test=app/'tests'/f"test_{spec['slug']}{'_pqc' if pqc else ''}.py"; src=test.read_text(encoding='utf-8')
   block=f'''\n\ndef test_{method}_enforces_{spec['slug']}_workflow(tmp_path):
    from {pkg} import {cls}
    record=dict(RECORD,state='reviewed'); app={cls}(tmp_path/'domain.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.{method}(record['record_id'], {gc})
    assert result['state']=='released'
    with __import__('sqlite3').connect(app.path) as db: event=db.execute('SELECT previous_state,next_state FROM workflow_events').fetchone()
    assert event==('reviewed','released')

def test_{method}_rejects_{spec['slug']}_workflow_violation(tmp_path):
    from {pkg} import {cls}
    record=dict(RECORD,state='reviewed'); app={cls}(tmp_path/'domain.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises((ValueError,PermissionError)):
        app.{method}(record['record_id'], {bc})
    assert app.retrieve(record['record_id'])['state']=='reviewed'
'''
   if f'def test_{method}_enforces_' not in src:test.write_text(src.rstrip()+block,encoding='utf-8',newline='\n')
  task=next(t for t in tasks if t['repository_id']==rid and t['task_id']==f'OPMB-{n*10:04d}'); task['function_names']=[method]; task['source_files'].append(f"migrated_reference/{spec['slug']}_pqc/service.py"); task['expected_behavior']=[f"Enforce {spec['purpose']}","Persist the signed domain decision and state update atomically.","Reject failed policy conditions without mutating workflow state."]; task['verification_procedure']=[f"Run both original and PQC tests for {method}, including success and policy rejection.","Run batch schema/path validation and inspect recorded suite evidence."]; (ROOT/task['task_path']/'task.json').write_text(json.dumps(task,indent=2)+'\n',encoding='utf-8')
  readme=app/'README.md'; text=readme.read_text(encoding='utf-8'); readme.write_text(text+f"\n## Domain workflow\n\nOriginal and PQC services implement `{method}` for this application's documented operational rule. The decision requires signed approval and is recorded atomically with the workflow transition.\n",encoding='utf-8',newline='\n') if '## Domain workflow' not in text else None
 (TEAM/'batch-03'/'tasks.json').write_text(json.dumps(tasks,indent=2)+'\n',encoding='utf-8'); (TEAM/'batch-03'/'repositories.json').write_text(json.dumps(repos,indent=2)+'\n',encoding='utf-8'); print('Added ten distinct workflows for REPO-261..270.')
if __name__=='__main__':main()
