"""License issuance, offline verification, and revocation snapshot creation."""
import sqlite3
from pathlib import Path
from .crypto import canonical_license,sign_license,verify_license
class LicenseDesk:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS licenses(license_id TEXT PRIMARY KEY,product TEXT NOT NULL,installation TEXT NOT NULL,features TEXT NOT NULL,issued_at INTEGER NOT NULL,expires_at INTEGER NOT NULL,record BLOB NOT NULL,signature BLOB NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS revocation_log(license_id TEXT PRIMARY KEY,revoked_at INTEGER NOT NULL,reason TEXT NOT NULL)")
 def issue(self,lid,product,installation,features,issued_at,expires_at,private):
  record=canonical_license(lid,product,installation,features,issued_at,expires_at);sig=sign_license(record,private)
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO licenses VALUES(?,?,?,?,?,?,?,?, 'active')",(lid,product,installation,','.join(sorted(set(features))),issued_at,expires_at,record,sig))
 def revoke(self,lid,reason,*,now):
  if not reason:raise ValueError('reason required')
  with sqlite3.connect(self.path) as db:
   cur=db.execute("UPDATE licenses SET status='revoked' WHERE license_id=? AND status='active'",(lid,))
   if cur.rowcount!=1:return False
   db.execute("INSERT INTO revocation_log VALUES(?,?,?)",(lid,now,reason));return True
 def verify_offline(self,lid,product,installation,required_feature,public,*,now,revoked_snapshot=None):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT product,installation,features,issued_at,expires_at,record,signature,status FROM licenses WHERE license_id=?",(lid,)).fetchone()
  if r is None or r[7]!='active' or lid in (revoked_snapshot or set()):return False
  if (r[0],r[1])!=(product,installation) or required_feature not in r[2].split(',') or not (r[3]<=now<r[4]):return False
  return verify_license(r[5],r[6],public)
 def revocation_snapshot(self):
  with sqlite3.connect(self.path) as db:return {r[0] for r in db.execute("SELECT license_id FROM revocation_log").fetchall()}
