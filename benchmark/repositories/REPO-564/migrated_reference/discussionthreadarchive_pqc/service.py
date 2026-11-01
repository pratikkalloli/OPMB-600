"""Persistent archive_record lifecycle with domain validation."""
import json, sqlite3
from pathlib import Path
from .crypto import canonical_claims, sign_claims, verify_claims

def validate_claims(c: dict) -> None:
    required=['archive_id', 'workspace_id', 'thread_id', 'message_root', 'item_count', 'archived_at']
    if set(c) != set(required): raise ValueError("claims do not match the archive_record schema")
    if not c['workspace_id'] or not c['thread_id']: raise ValueError('workspace and thread are required')
    if len(c['message_root']) != 64 or c['item_count'] < 1: raise ValueError('invalid message root or item count')

class DiscussionThreadArchivePQC:
    def __init__(self, path: str | Path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db: db.execute("CREATE TABLE IF NOT EXISTS records(record_id TEXT PRIMARY KEY,payload BLOB NOT NULL,signature BLOB NOT NULL,active INTEGER NOT NULL)")

    def issue(self, claims: dict, private) -> None:
        validate_claims(claims)
        payload=canonical_claims(claims); signature=sign_claims(claims,private)
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO records VALUES(?,?,?,1)",(claims['archive_id'],payload,signature))

    def verify(self, record_id: str, public, *, expected: dict | None = None) -> bool:
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT payload,signature,active FROM records WHERE record_id=?",(record_id,)).fetchone()
        if row is None or not row[2]: return False
        try: claims=json.loads(row[0])
        except (ValueError,TypeError): return False
        if not isinstance(claims, dict) or claims.get('archive_id') != record_id: return False
        if expected and any(claims.get(k)!=v for k,v in expected.items()): return False
        try: validate_claims(claims)
        except (ValueError,TypeError,KeyError): return False
        return verify_claims(claims,row[1],public)

    def deactivate(self, record_id: str) -> bool:
        with sqlite3.connect(self.path) as db: return db.execute("UPDATE records SET active=0 WHERE record_id=? AND active=1",(record_id,)).rowcount==1
