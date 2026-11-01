"""Persistent event log for ProductionDeviationCase."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class ProductionDeviationCase:
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
        if row is None: raise KeyError("production deviation not found")
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
    def _commit_domain_decision(self, record, next_state, event_type, evidence):
        """Atomically persist a domain transition and its append-only decision evidence."""
        updated=transition_record(record,next_state)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS workflow_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, event_type TEXT NOT NULL, previous_state TEXT NOT NULL, next_state TEXT NOT NULL, evidence TEXT NOT NULL)")
            db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(updated,sort_keys=True),record['record_id']))
            db.execute("INSERT INTO workflow_events(record_id,event_type,previous_state,next_state,evidence) VALUES(?,?,?,?,?)",(record['record_id'],event_type,record['state'],next_state,json.dumps(evidence,sort_keys=True)))
        return updated

    def dispose_production_deviation(self, record_id, disposition, quality_manager_id, quality_public, containment_reference=None):
        """Require an independent quality manager and containment evidence for severe deviations."""
        record=self.retrieve(record_id)
        allowed={'repair','rework','scrap','use_as_is'}
        if record['state']!='contained': raise ValueError('deviation must be contained before disposition')
        if disposition not in allowed: raise ValueError('unsupported deviation disposition')
        if quality_manager_id==record['reporter_id']: raise PermissionError('reporter cannot approve their own deviation')
        if record['severity']=='critical' and not containment_reference: raise ValueError('critical deviation needs containment evidence')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('quality-manager signature is absent or invalid')
        return self._commit_domain_decision(record,'dispositioned','deviation_dispositioned',{'production_order':record['production_order'],'severity':record['severity'],'disposition':disposition,'quality_manager_id':quality_manager_id,'containment_reference':containment_reference})
