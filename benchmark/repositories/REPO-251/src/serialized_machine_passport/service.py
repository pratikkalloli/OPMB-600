"""Persistent event log for SerializedMachinePassport."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class SerializedMachinePassport:
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
        if row is None: raise KeyError("serialized machine passport not found")
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

    def transfer_machine_custody(self, record_id, **decision):
        # Apply the SerializedMachinePassport business decision and retain signed evidence.
        current_custodian=decision['current_custodian']
        new_custodian=decision['new_custodian']
        expected_sequence=decision['expected_sequence']
        maintenance_digest=decision['maintenance_digest']
        passport_public=decision['passport_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('passport must be reviewed before custody transfer')
        if type(expected_sequence) is not int or record['sequence']!=expected_sequence: raise ValueError('passport event sequence is stale')
        if not isinstance(new_custodian,str) or not new_custodian.strip() or new_custodian==current_custodian: raise ValueError('custodian transfer must identify a different named owner')
        if not isinstance(maintenance_digest,str) or len(maintenance_digest)!=64 or any(c not in '0123456789abcdef' for c in maintenance_digest): raise ValueError('maintenance attestation must be a SHA-256 digest')
        if not self.verify_approval(record_id,passport_public): raise PermissionError('current custodian passport signature is invalid')
        return self._commit_domain_decision(record,'released','machine_custody_transferred',{'from':current_custodian,'to':new_custodian,'sequence':expected_sequence,'maintenance_digest':maintenance_digest})
