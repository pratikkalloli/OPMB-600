"""Persistent key_rotation lifecycle with domain validation."""
import json, sqlite3
from pathlib import Path
from .crypto import canonical_claims, sign_claims, verify_claims

def validate_claims(c: dict) -> None:
    required=['rotation_id', 'workspace_id', 'previous_epoch', 'new_epoch', 'key_digest', 'issued_at']
    if set(c) != set(required): raise ValueError("claims do not match the key_rotation schema")
    if not c['workspace_id'] or len(c['key_digest']) != 64: raise ValueError('workspace and SHA-256 key digest are required')
    if c['previous_epoch'] < 0 or c['new_epoch'] != c['previous_epoch']+1: raise ValueError('workspace epoch must advance exactly once')

class SharedWorkspaceKeyRotationPQC:
    def __init__(self, path: str | Path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db: db.execute("CREATE TABLE IF NOT EXISTS records(record_id TEXT PRIMARY KEY,payload BLOB NOT NULL,signature BLOB NOT NULL,active INTEGER NOT NULL)")

    def issue(self, claims: dict, private) -> None:
        validate_claims(claims)
        payload=canonical_claims(claims); signature=sign_claims(claims,private)
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO records VALUES(?,?,?,1)",(claims['rotation_id'],payload,signature))

    def verify(self, record_id: str, public, *, expected: dict | None = None) -> bool:
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT payload,signature,active FROM records WHERE record_id=?",(record_id,)).fetchone()
        if row is None or not row[2]: return False
        try: claims=json.loads(row[0])
        except (ValueError,TypeError): return False
        if not isinstance(claims, dict) or claims.get('rotation_id') != record_id: return False
        if expected and any(claims.get(k)!=v for k,v in expected.items()): return False
        try: validate_claims(claims)
        except (ValueError,TypeError,KeyError): return False
        return verify_claims(claims,row[1],public)

    def deactivate(self, record_id: str) -> bool:
        with sqlite3.connect(self.path) as db: return db.execute("UPDATE records SET active=0 WHERE record_id=? AND active=1",(record_id,)).rowcount==1
