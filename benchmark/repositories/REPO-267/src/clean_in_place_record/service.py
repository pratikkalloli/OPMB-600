"""Persistent event log for CleanInPlaceRecord."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class CleanInPlaceRecord:
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
        if row is None: raise KeyError("clean in place record not found")
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
        updated=transition_record(record,next_state)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS workflow_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, event_type TEXT NOT NULL, previous_state TEXT NOT NULL, next_state TEXT NOT NULL, evidence TEXT NOT NULL)")
            db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(updated,sort_keys=True),record['record_id']))
            db.execute("INSERT INTO workflow_events(record_id,event_type,previous_state,next_state,evidence) VALUES(?,?,?,?,?)",(record['record_id'],event_type,record['state'],next_state,json.dumps(evidence,sort_keys=True)))
        return updated

    def release_vessel_after_cip(self, record_id, **decision):
        # Apply the CleanInPlaceRecord decision and preserve its signed evidence.
        phases=decision['phases']
        minimum_duration=decision['minimum_duration']
        next_lot=decision['next_lot']
        sanitation_public=decision['sanitation_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('clean-in-place cycle must be reviewed before vessel reuse')
        required=['pre_rinse','wash','post_rinse','sanitize']
        if not isinstance(phases,list) or [p.get('name') for p in phases if isinstance(p,dict)]!=required: raise ValueError('CIP phases must be completed in validated process order')
        if any(type(p.get('duration_seconds')) is not int or p['duration_seconds']<minimum_duration for p in phases): raise ValueError('a CIP phase did not meet its minimum validated duration')
        if any(p.get('result')!='pass' for p in phases): raise ValueError('failed CIP phase blocks vessel reuse')
        if not next_lot or not next_lot.strip(): raise ValueError('next production lot must be assigned before CIP release')
        if not self.verify_approval(record_id,sanitation_public): raise PermissionError('sanitation release signature is invalid')
        return self._commit_domain_decision(record,'released','cip_vessel_released',{'vessel_id':record['workcell_id'],'phase_count':len(phases),'next_lot':next_lot})
