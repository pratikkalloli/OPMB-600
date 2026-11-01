"""PQC-backed persistent event log for ToolWearForecastCase."""
import json, sqlite3
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record
class ToolWearForecastCasePQC:
    def _commit_domain_decision(self, record, next_state, event_type, evidence):
        updated=transition_record(record,next_state)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS workflow_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, event_type TEXT NOT NULL, previous_state TEXT NOT NULL, next_state TEXT NOT NULL, evidence TEXT NOT NULL)")
            db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(updated,sort_keys=True),record['record_id']))
            db.execute("INSERT INTO workflow_events(record_id,event_type,previous_state,next_state,evidence) VALUES(?,?,?,?,?)",(record['record_id'],event_type,record['state'],next_state,json.dumps(evidence,sort_keys=True)))
        return updated

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

    def decide_tool_wear_disposition(self, record_id, **decision):
        # Apply the ToolWearForecastCase business decision and retain signed evidence.
        safe_limit=decision['safe_limit']
        disposition=decision['disposition']
        replacement_serial=decision['replacement_serial']
        maintenance_public=decision['maintenance_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('wear case must be reviewed before disposition')
        if type(safe_limit) is not int or not 0<=safe_limit<=1000: raise ValueError('safe wear limit must be in the measured scale')
        if disposition=='return_to_service' and record['measured_value']>safe_limit: raise ValueError('worn tool exceeds the safe return-to-service limit')
        if disposition not in {'return_to_service','replace_and_retire'}: raise ValueError('unsupported tool maintenance disposition')
        if disposition=='replace_and_retire' and not replacement_serial: raise ValueError('replacement serial is required before retiring worn tool')
        if not self.verify_approval(record_id,maintenance_public): raise PermissionError('maintenance disposition signature is invalid')
        next_state='released' if disposition=='return_to_service' else 'retired'
        return self._commit_domain_decision(record,next_state,'tool_wear_disposition_decided',{'wear_measurement':record['measured_value'],'safe_limit':safe_limit,'disposition':disposition,'replacement_serial':replacement_serial})
