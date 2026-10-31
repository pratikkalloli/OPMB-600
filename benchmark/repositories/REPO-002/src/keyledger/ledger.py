"""Validated SQLite inventory with append-only signed lifecycle events."""
from __future__ import annotations
import json,sqlite3,time,uuid
from pathlib import Path
from .crypto import sign_audit_event,verify_audit_event,public_key_fingerprint
class KeyLedger:
    def __init__(self,path:str|Path,audit_private,audit_public):
        self.path=str(path); self.audit_private=audit_private; self.audit_public=audit_public
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS keys(key_id TEXT PRIMARY KEY,owner TEXT NOT NULL,purpose TEXT NOT NULL,algorithm TEXT NOT NULL,fingerprint TEXT NOT NULL,status TEXT NOT NULL,created INTEGER NOT NULL,expires INTEGER)")
            db.execute("CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT,key_id TEXT NOT NULL,kind TEXT NOT NULL,at INTEGER NOT NULL,payload BLOB NOT NULL,signature BLOB NOT NULL)")
    def register(self,owner:str,purpose:str,public,expires:int|None=None)->str:
        if not owner.strip() or not purpose.strip(): raise ValueError("owner and purpose are required")
        now=int(time.time())
        if expires is not None and expires<=now: raise ValueError("expiration must be in the future")
        key_id=uuid.uuid4().hex; fp=public_key_fingerprint(public)
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO keys VALUES(?,?,?,?,?,?,?,?)",(key_id,owner,purpose,"RSA",fp,"active",now,expires))
            payload=json.dumps({"id":key_id,"owner":owner,"purpose":purpose,"fingerprint":fp,"at":now},sort_keys=True,separators=(",",":")).encode(); sig=sign_audit_event(payload,self.audit_private)
            db.execute("INSERT INTO events(key_id,kind,at,payload,signature) VALUES(?,?,?,?,?)",(key_id,"registered",now,payload,sig))
        return key_id
    def rotate(self,key_id:str,new_public)->str:
        now=int(time.time()); fp=public_key_fingerprint(new_public)
        with sqlite3.connect(self.path) as db:
            row=db.execute("SELECT owner,purpose FROM keys WHERE key_id=? AND status='active'",(key_id,)).fetchone()
            if row is None: raise KeyError("active key not found")
            db.execute("UPDATE keys SET status='rotated' WHERE key_id=?",(key_id,)); new_id=uuid.uuid4().hex
            db.execute("INSERT INTO keys VALUES(?,?,?,?,?,?,?,NULL)",(new_id,row[0],row[1],"RSA",fp,"active",now))
            payload=json.dumps({"old":key_id,"new":new_id,"fingerprint":fp,"at":now},sort_keys=True,separators=(",",":")).encode(); sig=sign_audit_event(payload,self.audit_private)
            db.execute("INSERT INTO events(key_id,kind,at,payload,signature) VALUES(?,?,?,?,?)",(key_id,"rotated",now,payload,sig))
            db.execute("INSERT INTO events(key_id,kind,at,payload,signature) VALUES(?,?,?,?,?)",(new_id,"rotation_received",now,payload,sig))
        return new_id
    def revoke(self,key_id:str)->bool:
        with sqlite3.connect(self.path) as db:
            cur=db.execute("UPDATE keys SET status='revoked' WHERE key_id=? AND status='active'",(key_id,))
            if cur.rowcount:
                now=int(time.time()); payload=json.dumps({"id":key_id,"at":now,"status":"revoked"},sort_keys=True,separators=(",",":")).encode(); db.execute("INSERT INTO events(key_id,kind,at,payload,signature) VALUES(?,?,?,?,?)",(key_id,"revoked",now,payload,sign_audit_event(payload,self.audit_private)))
            return cur.rowcount==1
    def audit_valid(self,key_id:str)->bool:
        with sqlite3.connect(self.path) as db: rows=db.execute("SELECT payload,signature FROM events WHERE key_id=? ORDER BY seq",(key_id,)).fetchall()
        return bool(rows) and all(verify_audit_event(payload,sig,self.audit_public) for payload,sig in rows)
    def inventory(self):
        with sqlite3.connect(self.path) as db: return db.execute("SELECT key_id,owner,purpose,algorithm,fingerprint,status,created,expires FROM keys ORDER BY created,key_id").fetchall()
