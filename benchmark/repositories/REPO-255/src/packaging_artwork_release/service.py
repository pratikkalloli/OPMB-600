"""Persistent event log for PackagingArtworkRelease."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class PackagingArtworkRelease:
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
        if row is None: raise KeyError("packaging artwork release not found")
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

    def release_packaging_artwork(self, record_id, **decision):
        # Apply the PackagingArtworkRelease business decision and retain signed evidence.
        revision=decision['revision']
        approved_revisions=decision['approved_revisions']
        market=decision['market']
        authorized_markets=decision['authorized_markets']
        artwork_digest=decision['artwork_digest']
        regulatory_clearance=decision['regulatory_clearance']
        release_public=decision['release_public']
        record=self.retrieve(record_id)
        if record['state']!='reviewed': raise ValueError('artwork must be reviewed before print release')
        if revision not in set(approved_revisions): raise PermissionError('artwork revision is not on the approved master list')
        if market not in set(authorized_markets): raise PermissionError('market destination is not authorized for this artwork')
        if not isinstance(artwork_digest,str) or len(artwork_digest)!=64 or any(c not in '0123456789abcdef' for c in artwork_digest): raise ValueError('artwork proof must be identified by a SHA-256 digest')
        if record['review_class']=='critical' and not regulatory_clearance: raise PermissionError('critical label change requires regulatory clearance')
        if not self.verify_approval(record_id,release_public): raise PermissionError('artwork release signature is invalid')
        return self._commit_domain_decision(record,'released','packaging_artwork_released',{'revision':revision,'market':market,'artwork_digest':artwork_digest,'review_class':record['review_class']})
