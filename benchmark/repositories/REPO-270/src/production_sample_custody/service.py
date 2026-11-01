"""Persistent event log for ProductionSampleCustody."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class ProductionSampleCustody:
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
        if row is None: raise KeyError("production sample custody not found")
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

    def accept_retained_sample_custody(self, record_id, **decision):
        # Apply the ProductionSampleCustody decision and preserve its signed evidence.
        custody_events=decision['custody_events']
        disposition=decision['disposition']
        destruction_witness=decision['destruction_witness']
        custodian_public=decision['custodian_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('sample custody record must be reviewed before disposition')
        if not isinstance(custody_events,list) or not custody_events: raise ValueError('retained sample needs a custody event chain')
        if any(not isinstance(e,dict) or type(e.get('sequence')) is not int or not e.get('custodian') or not e.get('seal_id') for e in custody_events): raise ValueError('custody event is malformed or lacks seal attribution')
        if [e['sequence'] for e in custody_events]!=list(range(record['sequence'],record['sequence']+len(custody_events))): raise ValueError('sample custody chain has a sequence gap or replay')
        if disposition not in {'retain','archive','destroy'}: raise ValueError('unsupported retained-sample disposition')
        if disposition=='destroy' and not destruction_witness: raise PermissionError('sample destruction requires an independent witness')
        if not self.verify_approval(record_id,custodian_public): raise PermissionError('sample custody approval signature is invalid')
        return self._commit_domain_decision(record,'released','retained_sample_dispositioned',{'workcell_id':record['workcell_id'],'event_count':len(custody_events),'last_custodian':custody_events[-1]['custodian'],'disposition':disposition})
