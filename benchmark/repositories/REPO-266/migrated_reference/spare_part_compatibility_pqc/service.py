"""PQC-backed persistent event log for SparePartCompatibility."""
import json, sqlite3
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record
class SparePartCompatibilityPQC:
    def __init__(self,path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS records(record_id TEXT PRIMARY KEY, body TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS signatures(record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
    def register(self,record):
        item=validate_record(record)
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO records VALUES(?,?)",(item["record_id"],json.dumps(item,sort_keys=True)))
    def retrieve(self,record_id):
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT body FROM records WHERE record_id=?",(record_id,)).fetchone()
        if row is None: raise KeyError("record not found")
        return validate_record(json.loads(row[0]))
    def approve(self,record_id,private):
        record=self.retrieve(record_id); payload=canonical_record(record); sig=sign_record(record,private)
        with sqlite3.connect(self.path) as db: db.execute("INSERT OR REPLACE INTO signatures VALUES(?,?,?)",(record_id,payload,sig))
        return sig
    def verify_approval(self,record_id,public):
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT body,signature FROM signatures WHERE record_id=?",(record_id,)).fetchone()
        if row is None: return False
        return row[0]==canonical_record(self.retrieve(record_id)) and verify_record(self.retrieve(record_id),row[1],public)
    def advance(self,record_id,state):
        record=transition_record(self.retrieve(record_id),state)
        with sqlite3.connect(self.path) as db: db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(record,sort_keys=True),record_id))
        return record

    def _commit_domain_decision(self, record, next_state, event_type, evidence):
        updated=transition_record(record,next_state)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS workflow_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, event_type TEXT NOT NULL, previous_state TEXT NOT NULL, next_state TEXT NOT NULL, evidence TEXT NOT NULL)")
            db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(updated,sort_keys=True),record['record_id']))
            db.execute("INSERT INTO workflow_events(record_id,event_type,previous_state,next_state,evidence) VALUES(?,?,?,?,?)",(record['record_id'],event_type,record['state'],next_state,json.dumps(evidence,sort_keys=True)))
        return updated

    def approve_spare_part_fit(self, record_id, **decision):
        # Apply the SparePartCompatibility decision and preserve its signed evidence.
        machine_model=decision['machine_model']
        approved_models=decision['approved_models']
        machine_revision=decision['machine_revision']
        compatible_revisions=decision['compatible_revisions']
        safety_class=decision['safety_class']
        approved_safety_classes=decision['approved_safety_classes']
        engineering_public=decision['engineering_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('replacement part requires compatibility review')
        if machine_model not in set(approved_models): raise PermissionError('part is not approved for the installed machine model')
        if machine_revision not in set(compatible_revisions): raise ValueError('part compatibility does not cover this machine revision')
        if safety_class not in set(approved_safety_classes): raise PermissionError('replacement part safety class is not approved')
        if record['event_count']<1: raise ValueError('compatibility record must include at least one engineering review event')
        if not self.verify_approval(record_id,engineering_public): raise PermissionError('engineering compatibility approval is invalid')
        return self._commit_domain_decision(record,'released','spare_part_fit_approved',{'workcell_id':record['workcell_id'],'machine_model':machine_model,'machine_revision':machine_revision,'safety_class':safety_class})
