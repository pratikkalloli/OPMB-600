"""PQC-backed persistent event log for WorkOrderTraveler."""
import json, sqlite3
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record
class WorkOrderTravelerPQC:
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

    def complete_work_order_traveler(self, record_id, **decision):
        # Apply the WorkOrderTraveler decision and preserve its signed evidence.
        required_operations=decision['required_operations']
        station_signoffs=decision['station_signoffs']
        authorization_code=decision['authorization_code']
        quality_public=decision['quality_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('traveler must be reviewed before final station signoff')
        if not isinstance(required_operations,list) or not required_operations or len(set(required_operations))!=len(required_operations): raise ValueError('work order route must have unique required operations')
        if not isinstance(station_signoffs,dict) or not set(required_operations).issubset(station_signoffs): raise ValueError('traveler is missing one or more station signoffs')
        if any(not isinstance(station_signoffs[o],str) or not station_signoffs[o].strip() for o in required_operations): raise ValueError('station signoffs must identify qualified operators')
        if authorization_code!=record['authorization_code']: raise PermissionError('traveler is scoped to a different work order authorization')
        if not self.verify_approval(record_id,quality_public): raise PermissionError('final traveler signoff is invalid')
        return self._commit_domain_decision(record,'released','work_order_traveler_completed',{'workcell_id':record['workcell_id'],'operations':required_operations,'station_signoffs':station_signoffs,'authorization_code':authorization_code})
