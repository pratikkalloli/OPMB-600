"""Persistent event log for CleanroomProcessTicket."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class CleanroomProcessTicket:
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
        if row is None: raise KeyError("cleanroom ticket not found")
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

    def release_cleanroom_window(self, record_id, qualified_limit, cleanroom_public):
        """Release a cleanroom window within its qualified particle limit; quarantine excursions."""
        record=self.retrieve(record_id)
        if record['state']!='monitored': raise ValueError('cleanroom window must be monitored before release')
        if type(qualified_limit) is not int or qualified_limit<0: raise ValueError('qualified particle limit must be nonnegative')
        if not self.verify_approval(record_id,cleanroom_public): raise PermissionError('cleanroom review signature is absent or invalid')
        if record['particle_count']>qualified_limit:
            updated=self._commit_domain_decision(record,'quarantined','cleanroom_excursion_quarantined',{'room_id':record['room_id'],'particle_count':record['particle_count'],'qualified_limit':qualified_limit})
            raise RuntimeError(f"particle excursion quarantined in {updated['room_id']}")
        return self._commit_domain_decision(record,'released','cleanroom_window_released',{'room_id':record['room_id'],'particle_count':record['particle_count'],'qualified_limit':qualified_limit,'sampling_interval':record['sampling_interval']})
