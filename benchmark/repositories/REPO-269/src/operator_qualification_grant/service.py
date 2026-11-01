"""Persistent event log for OperatorQualificationGrant."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class OperatorQualificationGrant:
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
        if row is None: raise KeyError("operator qualification grant not found")
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

    def grant_operator_qualification(self, record_id, **decision):
        # Apply the OperatorQualificationGrant decision and preserve its signed evidence.
        now_epoch=decision['now_epoch']
        expiry_epoch=decision['expiry_epoch']
        requested_scope=decision['requested_scope']
        qualified_scope=decision['qualified_scope']
        training_digest=decision['training_digest']
        qualification_public=decision['qualification_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('operator qualification evidence must be reviewed before grant')
        if type(now_epoch) is not int or type(expiry_epoch) is not int or expiry_epoch<=now_epoch: raise ValueError('qualification is expired or has an invalid validity interval')
        if not isinstance(requested_scope,set) or not requested_scope or not requested_scope.issubset(set(qualified_scope)): raise PermissionError('requested task scope exceeds demonstrated operator qualification')
        if training_digest!=record['evidence_digest']: raise ValueError('training evidence digest does not match the qualification record')
        if not self.verify_approval(record_id,qualification_public): raise PermissionError('qualification grant is missing authorized signoff')
        return self._commit_domain_decision(record,'released','operator_qualification_granted',{'workcell_id':record['workcell_id'],'scope':sorted(requested_scope),'expiry_epoch':expiry_epoch,'training_digest':training_digest})
