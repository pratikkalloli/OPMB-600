"""Persistent event log for QualityHoldRelease."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class QualityHoldRelease:
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
        if row is None: raise KeyError("quality hold release not found")
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

    def release_contained_quality_hold(self, record_id, **decision):
        # Apply the QualityHoldRelease decision and preserve its signed evidence.
        affected_lots=decision['affected_lots']
        recheck_measurements=decision['recheck_measurements']
        lower_limit=decision['lower_limit']
        upper_limit=decision['upper_limit']
        quality_manager_public=decision['quality_manager_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('quality hold must be reviewed after containment')
        if not isinstance(affected_lots,list) or not affected_lots or len(set(affected_lots))!=len(affected_lots): raise ValueError('containment scope must list unique affected lots')
        if not isinstance(recheck_measurements,list) or not recheck_measurements: raise ValueError('hold release requires documented reinspection measurements')
        if type(lower_limit) not in (int,float) or type(upper_limit) not in (int,float) or lower_limit>upper_limit: raise ValueError('reinspection acceptance range is invalid')
        if any(type(x) not in (int,float) or not lower_limit<=x<=upper_limit for x in recheck_measurements): raise ValueError('one or more reinspection results remain outside release limits')
        if not self.verify_approval(record_id,quality_manager_public): raise PermissionError('quality manager release authorization is invalid')
        return self._commit_domain_decision(record,'released','quality_hold_released',{'affected_lots':affected_lots,'measurements':recheck_measurements,'acceptance_range':[lower_limit,upper_limit]})
