"""Persistent event log for TorqueAuditLedger."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class TorqueAuditLedger:
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
        if row is None: raise KeyError("torque audit ledger not found")
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

    def reconcile_torque_readings(self, record_id, **decision):
        # Apply the TorqueAuditLedger business decision and retain signed evidence.
        production_job=decision['production_job']
        readings=decision['readings']
        quality_public=decision['quality_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('torque ledger must be reviewed before reconciliation')
        if not isinstance(readings,list) or not readings: raise ValueError('at least one signed tool reading is required')
        outside=[]
        for item in readings:
            if not isinstance(item,dict) or type(item.get('measured')) not in (int,float) or type(item.get('low')) not in (int,float) or type(item.get('high')) not in (int,float) or item['low']>item['high']: raise ValueError('malformed torque interval')
            if not item['low']<=item['measured']<=item['high']: outside.append(item)
        if any(not isinstance(x.get('disposition'),str) or not x['disposition'].strip() for x in outside): raise ValueError('every out-of-tolerance fastening needs a quality disposition')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('quality approval for torque readings is invalid')
        return self._commit_domain_decision(record,'released','torque_readings_reconciled',{'job_id':production_job,'reading_count':len(readings),'out_of_tolerance':len(outside),'dispositions':[x.get('disposition') for x in outside]})
