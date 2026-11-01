"""PQC-backed persistent event log for ConsumableShelfLifeCard."""
import json, sqlite3
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record
class ConsumableShelfLifeCardPQC:
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

    def release_process_consumable(self, record_id, **decision):
        # Apply the ConsumableShelfLifeCard decision and preserve its signed evidence.
        opened_epoch=decision['opened_epoch']
        expiry_epoch=decision['expiry_epoch']
        now_epoch=decision['now_epoch']
        max_open_seconds=decision['max_open_seconds']
        lot_revision=decision['lot_revision']
        warehouse_public=decision['warehouse_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('consumable shelf-life record must be reviewed before issue')
        if any(type(v) is not int for v in (opened_epoch,expiry_epoch,now_epoch,max_open_seconds)): raise ValueError('shelf-life timestamps and limit must be integer epochs')
        if opened_epoch<0 or expiry_epoch<=opened_epoch or max_open_seconds<=0: raise ValueError('invalid consumable shelf-life interval')
        if now_epoch<opened_epoch or now_epoch>=expiry_epoch or now_epoch-opened_epoch>=max_open_seconds: raise ValueError('consumable lot or opened container is expired')
        if lot_revision!=record['revision_epoch']: raise ValueError('consumable label revision does not match the approved lot card')
        if not self.verify_approval(record_id,warehouse_public): raise PermissionError('consumable issue lacks authorized shelf-life signoff')
        return self._commit_domain_decision(record,'released','process_consumable_issued',{'workcell_id':record['workcell_id'],'lot_revision':lot_revision,'opened_epoch':opened_epoch,'expiry_epoch':expiry_epoch,'issued_at':now_epoch})
