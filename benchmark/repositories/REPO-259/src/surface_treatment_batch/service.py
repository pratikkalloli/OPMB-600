"""Persistent event log for SurfaceTreatmentBatch."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class SurfaceTreatmentBatch:
    def _commit_domain_decision(self, record, next_state, event_type, evidence):
        updated=transition_record(record,next_state)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS workflow_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, event_type TEXT NOT NULL, previous_state TEXT NOT NULL, next_state TEXT NOT NULL, evidence TEXT NOT NULL)")
            db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(updated,sort_keys=True),record['record_id']))
            db.execute("INSERT INTO workflow_events(record_id,event_type,previous_state,next_state,evidence) VALUES(?,?,?,?,?)",(record['record_id'],event_type,record['state'],next_state,json.dumps(evidence,sort_keys=True)))
        return updated

    def __init__(self, path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS records(record_id TEXT PRIMARY KEY, body TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS signatures(record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
    def register(self, record):
        item=validate_record(record)
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO records VALUES(?,?)",(item["record_id"],json.dumps(item,sort_keys=True)))
    def retrieve(self, record_id):
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT body FROM records WHERE record_id=?",(record_id,)).fetchone()
        if row is None: raise KeyError("surface treatment batch not found")
        return validate_record(json.loads(row[0]))
    def approve(self, record_id, private):
        record=self.retrieve(record_id); payload=canonical_record(record); sig=sign_record(record,private)
        with sqlite3.connect(self.path) as db: db.execute("INSERT OR REPLACE INTO signatures VALUES(?,?,?)",(record_id,payload,sig))
        return sig
    def verify_approval(self, record_id, public):
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT body,signature FROM signatures WHERE record_id=?",(record_id,)).fetchone()
        if row is None: return False
        return verify_record(self.retrieve(record_id),row[1],public) and row[0]==canonical_record(self.retrieve(record_id))
    def advance(self, record_id, state):
        record=transition_record(self.retrieve(record_id),state)
        with sqlite3.connect(self.path) as db: db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(record,sort_keys=True),record_id))
        return record

    def release_surface_treatment_batch(self, record_id, **decision):
        # Apply the SurfaceTreatmentBatch business decision and retain signed evidence.
        component_lot=decision['component_lot']
        chemistry_code=decision['chemistry_code']
        qualified_chemistries=decision['qualified_chemistries']
        cure_temperature_c=decision['cure_temperature_c']
        minimum_temperature_c=decision['minimum_temperature_c']
        maximum_temperature_c=decision['maximum_temperature_c']
        cure_minutes=decision['cure_minutes']
        minimum_cure_minutes=decision['minimum_cure_minutes']
        process_public=decision['process_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('coating batch must be reviewed before downstream release')
        if chemistry_code not in set(qualified_chemistries): raise ValueError('coating chemistry is not qualified for the component')
        if type(cure_temperature_c) is not int or type(cure_minutes) is not int or cure_minutes<0: raise ValueError('cure measurements are malformed')
        if not minimum_temperature_c<=cure_temperature_c<=maximum_temperature_c or cure_minutes<minimum_cure_minutes: raise ValueError('coating cure cycle is outside the qualified process window')
        if record['measured_value']!=cure_temperature_c: raise ValueError('recorded batch measurement differs from witnessed cure temperature')
        if not self.verify_approval(record_id,process_public): raise PermissionError('surface-treatment process signoff is invalid')
        return self._commit_domain_decision(record,'released','surface_treatment_batch_released',{'chemistry_code':chemistry_code,'cure_temperature_c':cure_temperature_c,'cure_minutes':cure_minutes,'component_lot':component_lot})
