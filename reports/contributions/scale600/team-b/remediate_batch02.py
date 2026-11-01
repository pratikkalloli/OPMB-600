#!/usr/bin/env python3
"""Add purpose-specific workflow decisions for REPO-251..260."""
from __future__ import annotations
import ast, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
TEAM=Path(__file__).resolve().parent

WORKFLOWS={
251:("transfer_machine_custody", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('passport must be reviewed before custody transfer')
        if type(expected_sequence) is not int or record['sequence']!=expected_sequence: raise ValueError('passport event sequence is stale')
        if not isinstance(new_custodian,str) or not new_custodian.strip() or new_custodian==current_custodian: raise ValueError('custodian transfer must identify a different named owner')
        if not isinstance(maintenance_digest,str) or len(maintenance_digest)!=64 or any(c not in '0123456789abcdef' for c in maintenance_digest): raise ValueError('maintenance attestation must be a SHA-256 digest')
        if not self.verify_approval(record_id,passport_public): raise PermissionError('current custodian passport signature is invalid')
        return self._commit_domain_decision(record,'released','machine_custody_transferred',{'from':current_custodian,'to':new_custodian,'sequence':expected_sequence,'maintenance_digest':maintenance_digest})""", "current_custodian='operator-251', new_custodian='operator-252', expected_sequence=251, maintenance_digest='b'*64", "new_custodian=''"),
252:("reconcile_torque_readings", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('torque ledger must be reviewed before reconciliation')
        if not isinstance(readings,list) or not readings: raise ValueError('at least one signed tool reading is required')
        outside=[]
        for item in readings:
            if not isinstance(item,dict) or type(item.get('measured')) not in (int,float) or type(item.get('low')) not in (int,float) or type(item.get('high')) not in (int,float) or item['low']>item['high']: raise ValueError('malformed torque interval')
            if not item['low']<=item['measured']<=item['high']: outside.append(item)
        if any(not isinstance(x.get('disposition'),str) or not x['disposition'].strip() for x in outside): raise ValueError('every out-of-tolerance fastening needs a quality disposition')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('quality approval for torque readings is invalid')
        return self._commit_domain_decision(record,'released','torque_readings_reconciled',{'job_id':production_job,'reading_count':len(readings),'out_of_tolerance':len(outside),'dispositions':[x.get('disposition') for x in outside]})""", "production_job='JOB-252', readings=[{'measured':12,'low':10,'high':14},{'measured':16,'low':10,'high':14,'disposition':'recalibrate'}]", "readings=[{'measured':16,'low':10,'high':14}]"),
253:("decide_tool_wear_disposition", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('wear case must be reviewed before disposition')
        if type(safe_limit) is not int or not 0<=safe_limit<=1000: raise ValueError('safe wear limit must be in the measured scale')
        if disposition=='return_to_service' and record['measured_value']>safe_limit: raise ValueError('worn tool exceeds the safe return-to-service limit')
        if disposition not in {'return_to_service','replace_and_retire'}: raise ValueError('unsupported tool maintenance disposition')
        if disposition=='replace_and_retire' and not replacement_serial: raise ValueError('replacement serial is required before retiring worn tool')
        if not self.verify_approval(record_id,maintenance_public): raise PermissionError('maintenance disposition signature is invalid')
        next_state='released' if disposition=='return_to_service' else 'retired'
        return self._commit_domain_decision(record,next_state,'tool_wear_disposition_decided',{'wear_measurement':record['measured_value'],'safe_limit':safe_limit,'disposition':disposition,'replacement_serial':replacement_serial})""", "safe_limit=30, disposition='return_to_service', replacement_serial=None", "safe_limit=10, disposition='return_to_service', replacement_serial=None"),
254:("witness_furnace_soak_window", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('heat-treatment cycle must be reviewed before release')
        if not isinstance(samples,list) or len(samples)<2: raise ValueError('cycle needs ordered temperature samples')
        if any(not isinstance(x,(tuple,list)) or len(x)!=2 or type(x[0]) is not int or type(x[1]) is not int for x in samples): raise ValueError('temperature samples must be integer time/temperature pairs')
        if any(samples[i][0]>=samples[i+1][0] for i in range(len(samples)-1)): raise ValueError('furnace sample times must strictly increase')
        if any(temp<minimum_c or temp>maximum_c for _,temp in samples): raise ValueError('furnace cycle exceeded its qualified temperature window')
        if samples[-1][0]-samples[0][0]<minimum_soak_seconds: raise ValueError('furnace cycle did not meet minimum soak duration')
        if not self.verify_approval(record_id,process_public): raise PermissionError('process engineer cycle signature is invalid')
        return self._commit_domain_decision(record,'released','furnace_cycle_witnessed',{'batch_id':heat_batch,'sample_count':len(samples),'temperature_window':[minimum_c,maximum_c],'soak_seconds':samples[-1][0]-samples[0][0]})""", "heat_batch='HEAT-254', samples=[(0,700),(3600,710)], minimum_c=680, maximum_c=740, minimum_soak_seconds=1800", "samples=[(0,700),(3600,710)], minimum_c=680, maximum_c=740, minimum_soak_seconds=4000"),
255:("release_packaging_artwork", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('artwork must be reviewed before print release')
        if revision not in set(approved_revisions): raise PermissionError('artwork revision is not on the approved master list')
        if market not in set(authorized_markets): raise PermissionError('market destination is not authorized for this artwork')
        if not isinstance(artwork_digest,str) or len(artwork_digest)!=64 or any(c not in '0123456789abcdef' for c in artwork_digest): raise ValueError('artwork proof must be identified by a SHA-256 digest')
        if record['review_class']=='critical' and not regulatory_clearance: raise PermissionError('critical label change requires regulatory clearance')
        if not self.verify_approval(record_id,release_public): raise PermissionError('artwork release signature is invalid')
        return self._commit_domain_decision(record,'released','packaging_artwork_released',{'revision':revision,'market':market,'artwork_digest':artwork_digest,'review_class':record['review_class']})""", "revision='ART-255-R2', approved_revisions={'ART-255-R2'}, market='US', authorized_markets={'US','CA'}, artwork_digest=RECORD['evidence_digest'], regulatory_clearance=True", "revision='ART-255-R1', approved_revisions={'ART-255-R2'}, market='US', authorized_markets={'US'}, artwork_digest=RECORD['evidence_digest'], regulatory_clearance=True"),
256:("release_fixture_for_inspection", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('fixture schedule must be reviewed before production release')
        if type(now_epoch) is not int or type(due_epoch) is not int or due_epoch<=0: raise ValueError('inspection schedule epochs are invalid')
        if now_epoch>due_epoch: raise ValueError('fixture inspection evidence is overdue; production use is blocked')
        if inspection_revision!=record['revision_epoch']: raise ValueError('inspection record revision does not match scheduled revision')
        if not self.verify_approval(record_id,inspector_public): raise PermissionError('fixture inspection signoff is invalid')
        return self._commit_domain_decision(record,'released','fixture_inspection_current',{'workcell_id':record['workcell_id'],'revision':inspection_revision,'due_epoch':due_epoch,'checked_at':now_epoch})""", "now_epoch=100, due_epoch=200, inspection_revision=RECORD['revision_epoch']", "now_epoch=201, due_epoch=200, inspection_revision=RECORD['revision_epoch']"),
257:("accept_shift_handover", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('handover docket must be reviewed before transfer')
        if not outgoing_lead or not incoming_lead or outgoing_lead==incoming_lead: raise ValueError('handover requires distinct named shift leads')
        if not isinstance(open_actions,list) or any(not isinstance(x,dict) or not x.get('action_id') or x.get('owner')!=incoming_lead for x in open_actions): raise ValueError('every open safety or quality action must be assigned to the incoming lead')
        if not open_actions: raise ValueError('handover must explicitly enumerate outstanding actions')
        if not self.verify_approval(record_id,outgoing_public): raise PermissionError('outgoing shift lead signature is invalid')
        return self._commit_domain_decision(record,'released','shift_handover_accepted',{'workcell_id':record['workcell_id'],'outgoing_lead':outgoing_lead,'incoming_lead':incoming_lead,'open_action_ids':[x['action_id'] for x in open_actions],'evidence_digest':record['evidence_digest']})""", "outgoing_lead='lead-day', incoming_lead='lead-night', open_actions=[{'action_id':'SAFE-257-1','owner':'lead-night'}]", "outgoing_lead='lead-day', incoming_lead='lead-night', open_actions=[{'action_id':'SAFE-257-1','owner':'lead-day'}]"),
258:("authorize_wip_scrap", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('scrap voucher must be reviewed before authorization')
        if not isinstance(serials,list) or not serials or any(not isinstance(x,str) or not x.strip() for x in serials): raise ValueError('serialized work-in-process units are required')
        if len(set(serials))!=len(serials): raise ValueError('a serialized unit cannot be scrapped twice on one voucher')
        if type(authorized_quantity) is not int or authorized_quantity<1 or len(serials)>authorized_quantity: raise ValueError('scrap quantity exceeds production-order authorization')
        if not disposition_code or not disposition_code.strip(): raise ValueError('quality disposition is required')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('quality scrap authorization signature is invalid')
        return self._commit_domain_decision(record,'released','wip_scrap_authorized',{'workcell_id':record['workcell_id'],'serials':serials,'quantity':len(serials),'disposition':disposition_code})""", "serials=['WIP-258-A','WIP-258-B'], authorized_quantity=2, disposition_code='NCR-258-SCRAP'", "serials=['WIP-258-A','WIP-258-A'], authorized_quantity=2, disposition_code='NCR-258-SCRAP'"),
259:("release_surface_treatment_batch", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('coating batch must be reviewed before downstream release')
        if chemistry_code not in set(qualified_chemistries): raise ValueError('coating chemistry is not qualified for the component')
        if type(cure_temperature_c) is not int or type(cure_minutes) is not int or cure_minutes<0: raise ValueError('cure measurements are malformed')
        if not minimum_temperature_c<=cure_temperature_c<=maximum_temperature_c or cure_minutes<minimum_cure_minutes: raise ValueError('coating cure cycle is outside the qualified process window')
        if record['measured_value']!=cure_temperature_c: raise ValueError('recorded batch measurement differs from witnessed cure temperature')
        if not self.verify_approval(record_id,process_public): raise PermissionError('surface-treatment process signoff is invalid')
        return self._commit_domain_decision(record,'released','surface_treatment_batch_released',{'chemistry_code':chemistry_code,'cure_temperature_c':cure_temperature_c,'cure_minutes':cure_minutes,'component_lot':component_lot})""", "component_lot='LOT-259', chemistry_code='ZINC-NI', qualified_chemistries={'ZINC-NI'}, cure_temperature_c=25, minimum_temperature_c=20, maximum_temperature_c=30, cure_minutes=60, minimum_cure_minutes=45", "component_lot='LOT-259', chemistry_code='UNKNOWN', qualified_chemistries={'ZINC-NI'}, cure_temperature_c=25, minimum_temperature_c=20, maximum_temperature_c=30, cure_minutes=60, minimum_cure_minutes=45"),
260:("authorize_assembly_operation", """        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('assembly permit must be reviewed before operation authorization')
        required=set(required_operations); completed=set(completed_operations)
        if not required or not required.issubset(completed): raise ValueError('all predecessor assembly operations must be recorded')
        if len(completed_operations)!=len(completed): raise ValueError('duplicate predecessor operation evidence is not accepted')
        if type(next_sequence) is not int or next_sequence!=record['sequence']+1: raise ValueError('assembly operation sequence is not the immediate successor')
        if record['event_count']!=len(completed): raise ValueError('permit predecessor count does not match recorded operation count')
        if not self.verify_approval(record_id,production_public): raise PermissionError('production-control permit signature is invalid')
        return self._commit_domain_decision(record,'released','assembly_operation_authorized',{'workcell_id':record['workcell_id'],'required_operations':sorted(required),'completed_operations':sorted(completed),'authorized_sequence':next_sequence})""", "required_operations={'frame-fit','torque-check'}, completed_operations=['frame-fit','torque-check','seal','inspection'], next_sequence=RECORD['sequence']+1", "required_operations={'frame-fit','torque-check'}, completed_operations=['frame-fit'], next_sequence=RECORD['sequence']+1"),
}

def main()->None:
    tasks=json.loads((TEAM/'batch-02'/'tasks.json').read_text(encoding='utf-8'))
    repos=json.loads((TEAM/'batch-02'/'repositories.json').read_text(encoding='utf-8'))
    specs={s['repository_id']:s for s in json.loads((TEAM/'application_specs.json').read_text(encoding='utf-8'))}
    for n,(method,body,good,bad) in WORKFLOWS.items():
        rid=f'REPO-{n:03d}'; spec=specs[rid]; app=ROOT/'benchmark'/'repositories'/rid
        service=next(app.glob('src/*/service.py')); ref=next(app.glob('migrated_reference/*/service.py'))
        original_class=next(x.name for x in ast.walk(ast.parse(service.read_text())) if isinstance(x,ast.ClassDef))
        pqc_class=next(x.name for x in ast.walk(ast.parse(ref.read_text())) if isinstance(x,ast.ClassDef))
        good_kw={k.arg:ast.unparse(k.value) for k in ast.parse(f"f({good})",mode='eval').body.keywords}
        bad_kw={k.arg:ast.unparse(k.value) for k in ast.parse(f"f({bad})",mode='eval').body.keywords}
        public_params=sorted(set(re.findall(r"\b([a-z_]+_public)\b",body)))
        for p in public_params: good_kw[p]="signer.public_key()"; bad_kw[p]="signer.public_key()"
        good_call=', '.join(f'{k}={v}' for k,v in good_kw.items())
        bad_kw={**good_kw,**bad_kw}
        bad_call=', '.join(f'{k}={v}' for k,v in bad_kw.items())
        for path,cls in ((service,original_class),(ref,pqc_class)):
            src=path.read_text(encoding='utf-8')
            marker=f'    def {method}('
            if marker not in src:
                unpack=''.join(f"        {p}=decision['{p}']\n" for p in good_kw)
                src=src.rstrip()+f"\n\n    def {method}(self, record_id, **decision):\n        # Apply the {spec['name']} business decision and retain signed evidence.\n"+unpack+body+"\n"
                path.write_text(src,encoding='utf-8',newline='\n')
            if 'def _commit_domain_decision(' not in src:
                helper='''    def _commit_domain_decision(self, record, next_state, event_type, evidence):
        updated=transition_record(record,next_state)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS workflow_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, event_type TEXT NOT NULL, previous_state TEXT NOT NULL, next_state TEXT NOT NULL, evidence TEXT NOT NULL)")
            db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(updated,sort_keys=True),record['record_id']))
            db.execute("INSERT INTO workflow_events(record_id,event_type,previous_state,next_state,evidence) VALUES(?,?,?,?,?)",(record['record_id'],event_type,record['state'],next_state,json.dumps(evidence,sort_keys=True)))
        return updated

'''
                src=src.replace(marker,helper+marker,1)
                path.write_text(src,encoding='utf-8',newline='\n')
        for pqc in (False,True):
            test=app/'tests'/f"test_{spec['slug']}{'_pqc' if pqc else ''}.py"
            src=test.read_text(encoding='utf-8')
            cls=pqc_class if pqc else original_class
            pkg=f'migrated_reference.{spec["slug"]}_pqc.service' if pqc else f'{spec["slug"]}.service'
            block=f'''\n\ndef test_{method}_enforces_{spec['slug']}_policy(tmp_path):
    from {pkg} import {cls}
    record=dict(RECORD,state='reviewed'); app={cls}(tmp_path/'domain.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.{method}(record['record_id'], {good_call})
    assert result['state']=='released'
    with __import__('sqlite3').connect(app.path) as db:
        event=db.execute('SELECT event_type,previous_state,next_state FROM workflow_events').fetchone()
    assert event[0] and event[1:] == ('reviewed','released')

def test_{method}_rejects_{spec['slug']}_policy_violation_without_transition(tmp_path):
    from {pkg} import {cls}
    record=dict(RECORD,state='reviewed'); app={cls}(tmp_path/'domain.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises((ValueError,PermissionError)):
        app.{method}(record['record_id'], {bad_call})
    assert app.retrieve(record['record_id'])['state']=='reviewed'
'''
            if f'def test_{method}_enforces_' not in src: test.write_text(src.rstrip()+block,encoding='utf-8',newline='\n')
        transition=next(t for t in tasks if t['repository_id']==rid and t['task_id']==f"OPMB-{n*10:04d}")
        transition['function_names']=[method]
        transition['source_files'] += [f"migrated_reference/{spec['slug']}_pqc/service.py"]
        transition['expected_behavior']=[f"Enforce {spec['purpose']}","Record an application-specific signed decision with an atomic state and workflow-event update.","Reject policy violations without changing the record state."]
        transition['verification_procedure']=[f"Run both original and PQC test modules and verify {method} success, policy rejection, and unchanged state on rejection.","Run the batch path/schema validator and inspect generated evidence."]
        (ROOT/transition['task_path']/'task.json').write_text(json.dumps(transition,indent=2)+'\n',encoding='utf-8')
        readme=app/'README.md'; text=readme.read_text(encoding='utf-8')
        if '## Domain workflow' not in text: readme.write_text(text+f"\n## Domain workflow\n\nBoth the original and PQC services implement `{method}`. It enforces the application's stated business rule and records the decision with the signed record's workflow event.\n",encoding='utf-8',newline='\n')
    (TEAM/'batch-02'/'tasks.json').write_text(json.dumps(tasks,indent=2)+'\n',encoding='utf-8')
    (TEAM/'batch-02'/'repositories.json').write_text(json.dumps(repos,indent=2)+'\n',encoding='utf-8')
    print('Added ten distinct application workflow decisions and original/PQC tests for Batch 02.')

if __name__=='__main__': main()
