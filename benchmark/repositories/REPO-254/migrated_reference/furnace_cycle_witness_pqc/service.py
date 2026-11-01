"""PQC-backed persistent event log for FurnaceCycleWitness."""
import json, sqlite3
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record
class FurnaceCycleWitnessPQC:
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

    def witness_furnace_soak_window(self, record_id, **decision):
        # Apply the FurnaceCycleWitness business decision and retain signed evidence.
        heat_batch=decision['heat_batch']
        samples=decision['samples']
        minimum_c=decision['minimum_c']
        maximum_c=decision['maximum_c']
        minimum_soak_seconds=decision['minimum_soak_seconds']
        process_public=decision['process_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('heat-treatment cycle must be reviewed before release')
        if not isinstance(samples,list) or len(samples)<2: raise ValueError('cycle needs ordered temperature samples')
        if any(not isinstance(x,(tuple,list)) or len(x)!=2 or type(x[0]) is not int or type(x[1]) is not int for x in samples): raise ValueError('temperature samples must be integer time/temperature pairs')
        if any(samples[i][0]>=samples[i+1][0] for i in range(len(samples)-1)): raise ValueError('furnace sample times must strictly increase')
        if any(temp<minimum_c or temp>maximum_c for _,temp in samples): raise ValueError('furnace cycle exceeded its qualified temperature window')
        if samples[-1][0]-samples[0][0]<minimum_soak_seconds: raise ValueError('furnace cycle did not meet minimum soak duration')
        if not self.verify_approval(record_id,process_public): raise PermissionError('process engineer cycle signature is invalid')
        return self._commit_domain_decision(record,'released','furnace_cycle_witnessed',{'batch_id':heat_batch,'sample_count':len(samples),'temperature_window':[minimum_c,maximum_c],'soak_seconds':samples[-1][0]-samples[0][0]})
