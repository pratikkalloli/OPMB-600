"""Signed capability issuance, online revocation, and authorization."""
import sqlite3
from pathlib import Path
from .crypto import canonical_capability,sign_capability,verify_capability
class CapabilityGate:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:db.execute("CREATE TABLE IF NOT EXISTS capabilities(token_id TEXT PRIMARY KEY,principal TEXT NOT NULL,resource TEXT NOT NULL,action TEXT NOT NULL,expires_at INTEGER NOT NULL,payload BLOB NOT NULL,signature BLOB NOT NULL,status TEXT NOT NULL)")
 def issue(self,token_id,principal,resource,action,expires_at,private):
  p=canonical_capability(token_id,principal,resource,action,expires_at);sig=sign_capability(p,private)
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO capabilities VALUES(?,?,?,?,?,?,?,'active')",(token_id,principal,resource,action,expires_at,p,sig))
  return p,sig
 def revoke(self,token_id):
  with sqlite3.connect(self.path) as db:return db.execute("UPDATE capabilities SET status='revoked' WHERE token_id=? AND status='active'",(token_id,)).rowcount==1
 def authorize(self,token_id,principal,resource,action,public,*,now):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT principal,resource,action,expires_at,payload,signature,status FROM capabilities WHERE token_id=?",(token_id,)).fetchone()
  if r is None or r[6]!='active' or r[3]<=now:return False
  if (r[0],r[1],r[2])!=(principal,resource,action):return False
  return verify_capability(r[4],r[5],public)
 def status(self,token_id):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT status FROM capabilities WHERE token_id=?",(token_id,)).fetchone()
  return None if r is None else r[0]
