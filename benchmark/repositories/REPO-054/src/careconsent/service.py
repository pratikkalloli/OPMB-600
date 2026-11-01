"""Persist signed consent grants and revocations for synthetic subjects."""
import sqlite3,time
from pathlib import Path
from .crypto import canonical_consent,sign_consent,verify_consent
class CareConsent:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS grants(consent_id TEXT PRIMARY KEY,subject TEXT NOT NULL,study TEXT NOT NULL,scope TEXT NOT NULL,expires_at INTEGER NOT NULL,revision INTEGER NOT NULL,record BLOB NOT NULL,signature BLOB NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS revocations(consent_id TEXT PRIMARY KEY,revoked_at INTEGER NOT NULL,reason TEXT NOT NULL)")
 def grant(self,cid,subject,study,scope,expires_at,revision,private):
  record=canonical_consent(cid,subject,study,scope,expires_at,revision);sig=sign_consent(record,private)
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO grants VALUES(?,?,?,?,?,?,?,?,'active')",(cid,subject,study,scope,expires_at,revision,record,sig))
 def revoke(self,cid,reason,*,now=None):
  if not reason:raise ValueError('revocation reason required')
  with sqlite3.connect(self.path) as db:
   cur=db.execute("UPDATE grants SET status='revoked' WHERE consent_id=? AND status='active'",(cid,))
   if cur.rowcount!=1:return False
   db.execute("INSERT INTO revocations VALUES(?,?,?)",(cid,int(time.time()) if now is None else now,reason));return True
 def authorize(self,cid,subject,study,scope,public,*,now=None):
  with sqlite3.connect(self.path) as db:row=db.execute("SELECT subject,study,scope,expires_at,record,signature,status FROM grants WHERE consent_id=?",(cid,)).fetchone()
  if row is None or row[6]!='active':return False
  current=int(time.time()) if now is None else now
  return row[0]==subject and row[1]==study and scope in row[2].split(',') and row[3]>current and verify_consent(row[4],row[5],public)
 def revision(self,cid):
  with sqlite3.connect(self.path) as db:row=db.execute("SELECT revision FROM grants WHERE consent_id=?",(cid,)).fetchone()
  return None if row is None else row[0]
