#!/usr/bin/env python3
"""Add application-specific, signed manufacturing decisions to REPO-241..250."""
from __future__ import annotations
import ast,csv,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]; TEAM=Path(__file__).resolve().parent

HELPER='''
    def _commit_domain_decision(self, record, next_state, event_type, evidence):
        """Atomically persist a domain transition and its append-only decision evidence."""
        updated=transition_record(record,next_state)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS workflow_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, event_type TEXT NOT NULL, previous_state TEXT NOT NULL, next_state TEXT NOT NULL, evidence TEXT NOT NULL)")
            db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(updated,sort_keys=True),record['record_id']))
            db.execute("INSERT INTO workflow_events(record_id,event_type,previous_state,next_state,evidence) VALUES(?,?,?,?,?)",(record['record_id'],event_type,record['state'],next_state,json.dumps(evidence,sort_keys=True)))
        return updated
'''

CASES={
"REPO-241":{
"method":"release_recipe","state":"reviewed","body":'''    def release_recipe(self, record_id, expected_revision, quality_public):
        """Release only the reviewed recipe revision signed for this workcell."""
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('recipe must pass quality review before release')
        if type(expected_revision) is not int or record['revision']!=expected_revision: raise ValueError('recipe revision changed after review')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('quality signature is absent or invalid')
        return self._commit_domain_decision(record,'released','recipe_released',{'line_id':record['line_id'],'revision':record['revision'],'approver_id':record['approver_id']})
''',
"tests":'''def test_recipe_release_requires_signed_reviewed_revision(tmp_path):
    from workcell_recipe_vault.service import WorkcellRecipeVault
    record=dict(RECORD,state='reviewed'); app=WorkcellRecipeVault(tmp_path/'recipe.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    released=app.release_recipe(record['record_id'],record['revision'],signer.public_key())
    assert released['state']=='released'
    with __import__('sqlite3').connect(app.path) as db:
        event=db.execute('SELECT event_type,previous_state,next_state,evidence FROM workflow_events').fetchone()
    assert event[0:3]==('recipe_released','reviewed','released') and 'line_id' in event[3]
def test_recipe_release_rejects_revision_mismatch_without_transition(tmp_path):
    from workcell_recipe_vault.service import WorkcellRecipeVault
    record=dict(RECORD,state='reviewed'); app=WorkcellRecipeVault(tmp_path/'recipe.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(ValueError): app.release_recipe(record['record_id'],record['revision']+1,signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='reviewed'
'''},
"REPO-242":{
"method":"clear_production_line","state":"inspected","body":'''    def clear_production_line(self, record_id, active_shift, checklist, supervisor_public):
        """Clear a changeover only for its shift after every required check passes."""
        record=self.retrieve(record_id)
        required={'guards_secured','previous_product_removed','tools_accounted'}
        if record['state']!='inspected': raise ValueError('line must be inspected before clearance')
        if record['shift_id']!=active_shift: raise PermissionError('clearance belongs to another shift')
        if not isinstance(checklist,dict) or set(checklist)!=required or any(v is not True for v in checklist.values()): raise ValueError('all line-clearance checks must pass')
        if not self.verify_approval(record_id,supervisor_public): raise PermissionError('supervisor signature is absent or invalid')
        return self._commit_domain_decision(record,'cleared','line_cleared',{'line_id':record['line_id'],'shift_id':active_shift,'checks':checklist})
''',
"tests":'''def test_line_clearance_requires_shift_and_all_checks(tmp_path):
    from line_clearance_token.service import LineClearanceToken
    record=dict(RECORD,state='inspected'); app=LineClearanceToken(tmp_path/'line.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    checks={'guards_secured':True,'previous_product_removed':True,'tools_accounted':True}
    result=app.clear_production_line(record['record_id'],record['shift_id'],checks,signer.public_key())
    assert result['state']=='cleared'
    with __import__('sqlite3').connect(app.path) as db: assert db.execute('SELECT event_type FROM workflow_events').fetchone()[0]=='line_cleared'
def test_line_clearance_rejects_wrong_shift_or_incomplete_checklist(tmp_path):
    from line_clearance_token.service import LineClearanceToken
    record=dict(RECORD,state='inspected'); app=LineClearanceToken(tmp_path/'line.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(PermissionError): app.clear_production_line(record['record_id'],'another-shift',{'guards_secured':True,'previous_product_removed':True,'tools_accounted':True},signer.public_key())
    with pytest.raises(ValueError): app.clear_production_line(record['record_id'],record['shift_id'],{'guards_secured':True},signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='inspected'
'''},
"REPO-243":{
"method":"accept_fixture_calibration","state":"measured","body":'''    def accept_fixture_calibration(self, record_id, tolerance_microns, now_epoch, valid_until_epoch, calibration_public):
        """Accept a fixture only within tolerance and before its calibration expiry."""
        record=self.retrieve(record_id)
        if record['state']!='measured': raise ValueError('fixture must have a measurement before acceptance')
        if type(tolerance_microns) is not int or tolerance_microns<0 or record['measured_error_microns']>tolerance_microns: raise ValueError('fixture measurement exceeds shop tolerance')
        if type(now_epoch) is not int or type(valid_until_epoch) is not int or now_epoch>=valid_until_epoch: raise ValueError('calibration certificate is expired')
        if record['calibration_revision']<1 or not self.verify_approval(record_id,calibration_public): raise PermissionError('calibration revision lacks a valid technician signature')
        return self._commit_domain_decision(record,'accepted','fixture_calibration_accepted',{'fixture_id':record['fixture_id'],'error_microns':record['measured_error_microns'],'tolerance_microns':tolerance_microns,'valid_until_epoch':valid_until_epoch})
''',
"tests":'''def test_fixture_acceptance_enforces_tolerance_and_expiry(tmp_path):
    from fixture_calibration_dossier.service import FixtureCalibrationDossier
    record=dict(RECORD,state='measured'); app=FixtureCalibrationDossier(tmp_path/'fixture.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.accept_fixture_calibration(record['record_id'],40,100,200,signer.public_key())
    assert result['state']=='accepted'
    with __import__('sqlite3').connect(app.path) as db: evidence=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert 'tolerance_microns' in evidence and 'fixture_id' in evidence
def test_fixture_acceptance_rejects_out_of_tolerance_and_expired_certificate(tmp_path):
    from fixture_calibration_dossier.service import FixtureCalibrationDossier
    record=dict(RECORD,state='measured'); app=FixtureCalibrationDossier(tmp_path/'fixture.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(ValueError): app.accept_fixture_calibration(record['record_id'],10,100,200,signer.public_key())
    with pytest.raises(ValueError): app.accept_fixture_calibration(record['record_id'],40,200,200,signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='measured'
'''},
"REPO-244":{
"method":"issue_weld_procedure","state":"qualified","body":'''    def issue_weld_procedure(self, record_id, qualified_material_pairs, qualified_engineers, welding_public):
        """Issue a weld procedure only for a qualified material pair and engineer."""
        record=self.retrieve(record_id)
        if record['state']!='qualified': raise ValueError('weld procedure is not qualified')
        if record['material_pair'] not in set(qualified_material_pairs): raise PermissionError('material pairing is not qualified')
        if record['engineer_id'] not in set(qualified_engineers): raise PermissionError('welding engineer is not qualified')
        if not self.verify_approval(record_id,welding_public): raise PermissionError('welding engineer signature is absent or invalid')
        return self._commit_domain_decision(record,'issued','weld_procedure_issued',{'joint_class':record['joint_class'],'material_pair':record['material_pair'],'procedure_digest':record['procedure_digest'],'engineer_id':record['engineer_id']})
''',
"tests":'''def test_weld_procedure_issue_checks_pair_engineer_and_signature(tmp_path):
    from weld_procedure_release.service import WeldProcedureRelease
    record=dict(RECORD,state='qualified'); app=WeldProcedureRelease(tmp_path/'weld.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.issue_weld_procedure(record['record_id'],{record['material_pair']},{record['engineer_id']},signer.public_key())
    assert result['state']=='issued'
    with __import__('sqlite3').connect(app.path) as db: ev=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert record['procedure_digest'] in ev
def test_weld_procedure_rejects_unqualified_material_pair(tmp_path):
    from weld_procedure_release.service import WeldProcedureRelease
    record=dict(RECORD,state='qualified'); app=WeldProcedureRelease(tmp_path/'weld.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(PermissionError): app.issue_weld_procedure(record['record_id'],set(),{record['engineer_id']},signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='qualified'
'''},
"REPO-245":{
"method":"certify_batch_yield","state":"reconciled","body":'''    def certify_batch_yield(self, record_id, planned_units, quality_public):
        """Certify a lot only when inspected good and rejected counts reconcile."""
        record=self.retrieve(record_id)
        if record['state']!='reconciled': raise ValueError('batch must be reconciled before certification')
        good=record['good_units']; rejected=record['rejected_units']
        if type(planned_units) is not int or planned_units<0 or good<0 or rejected<0 or good+rejected!=planned_units: raise ValueError('batch yield does not reconcile to planned quantity')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('quality signoff is absent or invalid')
        return self._commit_domain_decision(record,'certified','batch_yield_certified',{'batch_id':record['batch_id'],'good_units':good,'rejected_units':rejected,'inspection_station':record['inspection_station']})
''',
"tests":'''def test_batch_yield_certificate_reconciles_counts_and_audits(tmp_path):
    from batch_yield_certificate.service import BatchYieldCertificate
    record=dict(RECORD,state='reconciled'); app=BatchYieldCertificate(tmp_path/'yield.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.certify_batch_yield(record['record_id'],record['good_units']+record['rejected_units'],signer.public_key())
    assert result['state']=='certified'
    with __import__('sqlite3').connect(app.path) as db: ev=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert 'good_units' in ev and 'rejected_units' in ev
def test_batch_yield_rejects_unreconciled_quantity(tmp_path):
    from batch_yield_certificate.service import BatchYieldCertificate
    record=dict(RECORD,state='reconciled'); app=BatchYieldCertificate(tmp_path/'yield.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(ValueError): app.certify_batch_yield(record['record_id'],record['good_units']+record['rejected_units']+1,signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='reconciled'
'''},
"REPO-246":{
"method":"return_tool_to_service","state":"changed","body":'''    def return_tool_to_service(self, record_id, approved_serials, supervisor_public):
        """Return a tool to production only after the authorized serial is changed."""
        record=self.retrieve(record_id)
        if record['state']!='changed': raise ValueError('tool change must be confirmed before return to service')
        if record['tool_serial'] not in set(approved_serials): raise PermissionError('tool serial is not approved for this cell')
        if not record['reason_code'].strip(): raise ValueError('tool change reason is required')
        if not self.verify_approval(record_id,supervisor_public): raise PermissionError('supervisor authorization is absent or invalid')
        return self._commit_domain_decision(record,'returned_to_service','tool_returned_to_service',{'cell_id':record['cell_id'],'tool_serial':record['tool_serial'],'technician_id':record['technician_id'],'reason_code':record['reason_code']})
''',
"tests":'''def test_tool_return_requires_authorized_serial_and_signed_change(tmp_path):
    from tool_change_authorization.service import ToolChangeAuthorization
    record=dict(RECORD,state='changed'); app=ToolChangeAuthorization(tmp_path/'tool.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.return_tool_to_service(record['record_id'],{record['tool_serial']},signer.public_key())
    assert result['state']=='returned_to_service'
    with __import__('sqlite3').connect(app.path) as db: ev=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert record['tool_serial'] in ev and record['cell_id'] in ev
def test_tool_return_rejects_unapproved_serial_without_mutation(tmp_path):
    from tool_change_authorization.service import ToolChangeAuthorization
    record=dict(RECORD,state='changed'); app=ToolChangeAuthorization(tmp_path/'tool.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(PermissionError): app.return_tool_to_service(record['record_id'],set(),signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='changed'
'''},
"REPO-247":{
"method":"release_cleanroom_window","state":"monitored","body":'''    def release_cleanroom_window(self, record_id, qualified_limit, cleanroom_public):
        """Release a cleanroom window within its qualified particle limit; quarantine excursions."""
        record=self.retrieve(record_id)
        if record['state']!='monitored': raise ValueError('cleanroom window must be monitored before release')
        if type(qualified_limit) is not int or qualified_limit<0: raise ValueError('qualified particle limit must be nonnegative')
        if not self.verify_approval(record_id,cleanroom_public): raise PermissionError('cleanroom review signature is absent or invalid')
        if record['particle_count']>qualified_limit:
            updated=self._commit_domain_decision(record,'quarantined','cleanroom_excursion_quarantined',{'room_id':record['room_id'],'particle_count':record['particle_count'],'qualified_limit':qualified_limit})
            raise RuntimeError(f"particle excursion quarantined in {updated['room_id']}")
        return self._commit_domain_decision(record,'released','cleanroom_window_released',{'room_id':record['room_id'],'particle_count':record['particle_count'],'qualified_limit':qualified_limit,'sampling_interval':record['sampling_interval']})
''',
"tests":'''def test_cleanroom_release_requires_in_limit_signed_sample(tmp_path):
    from cleanroom_process_ticket.service import CleanroomProcessTicket
    record=dict(RECORD,state='monitored'); app=CleanroomProcessTicket(tmp_path/'cleanroom.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.release_cleanroom_window(record['record_id'],record['particle_count'],signer.public_key())
    assert result['state']=='released'
    with __import__('sqlite3').connect(app.path) as db: assert db.execute('SELECT event_type FROM workflow_events').fetchone()[0]=='cleanroom_window_released'
def test_cleanroom_excursion_is_quarantined_and_audited(tmp_path):
    from cleanroom_process_ticket.service import CleanroomProcessTicket
    record=dict(RECORD,state='monitored'); app=CleanroomProcessTicket(tmp_path/'cleanroom.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(RuntimeError): app.release_cleanroom_window(record['record_id'],record['particle_count']-1,signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='quarantined'
    with __import__('sqlite3').connect(app.path) as db: assert db.execute('SELECT event_type FROM workflow_events').fetchone()[0]=='cleanroom_excursion_quarantined'
'''},
"REPO-248":{
"method":"dispose_production_deviation","state":"contained","body":'''    def dispose_production_deviation(self, record_id, disposition, quality_manager_id, quality_public, containment_reference=None):
        """Require an independent quality manager and containment evidence for severe deviations."""
        record=self.retrieve(record_id)
        allowed={'repair','rework','scrap','use_as_is'}
        if record['state']!='contained': raise ValueError('deviation must be contained before disposition')
        if disposition not in allowed: raise ValueError('unsupported deviation disposition')
        if quality_manager_id==record['reporter_id']: raise PermissionError('reporter cannot approve their own deviation')
        if record['severity']=='critical' and not containment_reference: raise ValueError('critical deviation needs containment evidence')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('quality-manager signature is absent or invalid')
        return self._commit_domain_decision(record,'dispositioned','deviation_dispositioned',{'production_order':record['production_order'],'severity':record['severity'],'disposition':disposition,'quality_manager_id':quality_manager_id,'containment_reference':containment_reference})
''',
"tests":'''def test_deviation_disposition_requires_independent_approval(tmp_path):
    from production_deviation_case.service import ProductionDeviationCase
    record=dict(RECORD,state='contained'); app=ProductionDeviationCase(tmp_path/'deviation.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.dispose_production_deviation(record['record_id'],'rework','quality-lead-2',signer.public_key())
    assert result['state']=='dispositioned'
    with __import__('sqlite3').connect(app.path) as db: ev=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert 'quality_manager_id' in ev and 'disposition' in ev
def test_deviation_rejects_reporter_self_approval_and_bad_disposition(tmp_path):
    from production_deviation_case.service import ProductionDeviationCase
    record=dict(RECORD,state='contained'); app=ProductionDeviationCase(tmp_path/'deviation.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(PermissionError): app.dispose_production_deviation(record['record_id'],'scrap',record['reporter_id'],signer.public_key())
    with pytest.raises(ValueError): app.dispose_production_deviation(record['record_id'],'unknown','quality-lead-2',signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='contained'
'''},
"REPO-249":{
"method":"arm_machine_interlock","state":"reviewed","body":'''    def arm_machine_interlock(self, record_id, active_epoch, active_safety_case_digest, safety_public):
        """Arm a restart permit only for the currently active interlock and safety case."""
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('safety case must be reviewed before arming')
        if type(active_epoch) is not int or record['interlock_epoch']!=active_epoch: raise PermissionError('interlock permit is stale')
        if record['safety_case_digest']!=active_safety_case_digest: raise PermissionError('permit does not match the active safety case')
        if not self.verify_approval(record_id,safety_public): raise PermissionError('safety officer signature is absent or invalid')
        return self._commit_domain_decision(record,'armed','machine_interlock_armed',{'machine_id':record['machine_id'],'interlock_epoch':active_epoch,'safety_case_digest':active_safety_case_digest,'safety_officer_id':record['safety_officer_id']})
''',
"tests":'''def test_interlock_arm_requires_current_epoch_and_signed_case(tmp_path):
    from machine_interlock_permit.service import MachineInterlockPermit
    record=dict(RECORD,state='reviewed'); app=MachineInterlockPermit(tmp_path/'interlock.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.arm_machine_interlock(record['record_id'],record['interlock_epoch'],record['safety_case_digest'],signer.public_key())
    assert result['state']=='armed'
    with __import__('sqlite3').connect(app.path) as db: ev=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert 'interlock_epoch' in ev and 'safety_case_digest' in ev
def test_interlock_arm_rejects_stale_epoch_and_superseded_case(tmp_path):
    from machine_interlock_permit.service import MachineInterlockPermit
    record=dict(RECORD,state='reviewed'); app=MachineInterlockPermit(tmp_path/'interlock.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(PermissionError): app.arm_machine_interlock(record['record_id'],record['interlock_epoch']+1,record['safety_case_digest'],signer.public_key())
    with pytest.raises(PermissionError): app.arm_machine_interlock(record['record_id'],record['interlock_epoch'],'f'*64,signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='reviewed'
'''},
"REPO-250":{
"method":"consume_component_lot","state":"verified","body":'''    def consume_component_lot(self, record_id, next_receipt_sequence, approved_material_digests, inspector_public):
        """Consume only a verified component lot with approved provenance and expected sequence."""
        record=self.retrieve(record_id)
        if record['state']!='verified': raise ValueError('component lot must pass receiving verification')
        if record['material_digest'] not in set(approved_material_digests): raise PermissionError('material provenance digest is not approved')
        if type(next_receipt_sequence) is not int or record['receipt_sequence']!=next_receipt_sequence: raise ValueError('receipt sequence is stale or out of order')
        if not self.verify_approval(record_id,inspector_public): raise PermissionError('receiving inspection signature is absent or invalid')
        return self._commit_domain_decision(record,'consumed','component_lot_consumed',{'component_id':record['component_id'],'source_lot':record['source_lot'],'material_digest':record['material_digest'],'receipt_sequence':record['receipt_sequence']})
''',
"tests":'''def test_component_lot_consumption_checks_provenance_and_sequence(tmp_path):
    from component_trace_lot.service import ComponentTraceLot
    record=dict(RECORD,state='verified'); app=ComponentTraceLot(tmp_path/'trace.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    result=app.consume_component_lot(record['record_id'],record['receipt_sequence'],{record['material_digest']},signer.public_key())
    assert result['state']=='consumed'
    with __import__('sqlite3').connect(app.path) as db: ev=db.execute('SELECT evidence FROM workflow_events').fetchone()[0]
    assert record['source_lot'] in ev and record['material_digest'] in ev
def test_component_lot_rejects_unapproved_digest_and_sequence(tmp_path):
    from component_trace_lot.service import ComponentTraceLot
    record=dict(RECORD,state='verified'); app=ComponentTraceLot(tmp_path/'trace.db'); app.register(record)
    signer=generate_signer(); app.approve(record['record_id'],signer)
    with pytest.raises(PermissionError): app.consume_component_lot(record['record_id'],record['receipt_sequence'],set(),signer.public_key())
    with pytest.raises(ValueError): app.consume_component_lot(record['record_id'],record['receipt_sequence']+1,{record['material_digest']},signer.public_key())
    assert app.retrieve(record['record_id'])['state']=='verified'
''' }
}

def main()->None:
    tasks=json.loads((TEAM/'batch-01'/'tasks.json').read_text(encoding='utf-8')); repos=json.loads((TEAM/'batch-01'/'repositories.json').read_text(encoding='utf-8'))
    for rid,c in CASES.items():
        app=ROOT/'benchmark'/'repositories'/rid; pkg=next((app/'src').iterdir()).name; refpkg=next((app/'migrated_reference').iterdir()).name; title=next(r['name'] for r in repos if r['repository_id']==rid)
        for service_path, cls in ((app/'src'/pkg/'service.py',title),(app/'migrated_reference'/refpkg/'service.py',title+'PQC')):
            text=service_path.read_text(encoding='utf-8')
            if f"def {c['method']}(" not in text:
                if 'def _commit_domain_decision(' not in text: text=text.rstrip()+HELPER
                text=text.rstrip()+"\n\n"+c['body']
                service_path.write_text(text,encoding='utf-8',newline='\n')
        for is_pqc in (False,True):
            testpath=app/'tests'/f"test_{pkg}{'_pqc' if is_pqc else ''}.py"
            text=testpath.read_text(encoding='utf-8')
            block=c['tests'].replace(f'from {pkg}.service import {title}',f'from {refpkg}.service import {title}PQC') if is_pqc else c['tests']
            if is_pqc: block=block.replace(f'{title}(',f'{title}PQC(')
            marker='def test_' + c['method']
            if marker not in text: testpath.write_text(text.rstrip()+"\n\n"+block,encoding='utf-8',newline='\n')
        # Attach the domain transition to the existing transition-migration task.
        own=[t for t in tasks if t['repository_id']==rid]
        transition=next(t for t in own if t['function_names']==['transition_record'])
        transition['function_names']=[c['method']]
        if f"src/{pkg}/service.py" not in transition['source_files']: transition['source_files'].append(f"src/{pkg}/service.py")
        if f"migrated_reference/{refpkg}/service.py" not in transition['source_files']: transition['source_files'].append(f"migrated_reference/{refpkg}/service.py")
        transition['cryptographic_operation']=f"Signed {title} domain transition and append-only decision evidence"
        transition['migration_objective']=f"Migrate {title} {c['method'].replace('_',' ')} authorization from RSA-PSS to ML-DSA-65 while preserving its application-specific business invariant."
        transition['expected_behavior']=[f"Permit the {title} workflow only when its domain preconditions and signed approval are valid.","Persist the state transition and decision evidence atomically.","Reject stale, unauthorized, malformed, or out-of-policy decisions without changing application state."]
        transition['verification_procedure']=["Run the original and PQC test modules separately.",f"Exercise {c['method']} success, policy rejection, signature rejection, and persisted decision evidence."]
        (ROOT/transition['task_path']/'task.json').write_text(json.dumps(transition,indent=2)+'\n',encoding='utf-8')
        # README describes the newly implemented operation and its invariant.
        readme=app/'README.md'; rtext=readme.read_text(encoding='utf-8')
        if f"## Domain workflow" not in rtext:
            rtext += f"\n## Domain workflow\n\nThe original and PQC service layers expose `{c['method']}`. This operation verifies the current signed record, enforces the application's business-specific policy, and records the resulting decision and evidence transactionally.\n"
            readme.write_text(rtext,encoding='utf-8',newline='\n')
    (TEAM/'batch-01'/'tasks.json').write_text(json.dumps(tasks,indent=2)+'\n',encoding='utf-8')
    (TEAM/'batch-01'/'repositories.json').write_text(json.dumps(repos,indent=2)+'\n',encoding='utf-8')
    print('Added ten application-specific signed workflow decisions to original and PQC services and tests.')
if __name__=='__main__': main()
