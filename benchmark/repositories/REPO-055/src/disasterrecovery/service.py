"""Snapshot planning, verified restoration, key rotation, and audit."""
import hashlib,sqlite3
from pathlib import Path
from .crypto import canonical_recovery_manifest,sign_recovery_manifest,verify_recovery_manifest,seal_snapshot,open_snapshot,export_recovery_signer,load_recovery_signer,export_recovery_recipient,load_recovery_recipient
class DisasterRecovery:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS systems(system_id TEXT PRIMARY KEY,current_key INTEGER NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS recovery_keys(system_id TEXT NOT NULL,key_version INTEGER NOT NULL,recipient_key BLOB NOT NULL,signer_key BLOB NOT NULL,PRIMARY KEY(system_id,key_version))")
   db.execute("CREATE TABLE IF NOT EXISTS snapshots(snapshot_id TEXT PRIMARY KEY,system_id TEXT NOT NULL,created_at INTEGER NOT NULL,key_version INTEGER NOT NULL,encapsulation BLOB NOT NULL,nonce BLOB NOT NULL,ciphertext BLOB NOT NULL,manifest BLOB NOT NULL,signature BLOB NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS restores(restore_id INTEGER PRIMARY KEY AUTOINCREMENT,snapshot_id TEXT NOT NULL,system_id TEXT NOT NULL,restored_at INTEGER NOT NULL,status TEXT NOT NULL)")
 def register_system(self,system_id,recipient_public,signer_public):
  with sqlite3.connect(self.path) as db:
   db.execute("INSERT INTO systems VALUES(?,1,'active')",(system_id,));db.execute("INSERT INTO recovery_keys VALUES(?,1,?,?)",(system_id,export_recovery_recipient(recipient_public),export_recovery_signer(signer_public)))
 def rotate_keys(self,system_id,recipient_public,signer_public):
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT current_key,status FROM systems WHERE system_id=?",(system_id,)).fetchone()
   if row is None or row[1]!='active':raise PermissionError('recovery system inactive')
   v=row[0]+1;db.execute("INSERT INTO recovery_keys VALUES(?,?,?,?)",(system_id,v,export_recovery_recipient(recipient_public),export_recovery_signer(signer_public)));db.execute("UPDATE systems SET current_key=? WHERE system_id=?",(v,system_id));return v
 def create_snapshot(self,snapshot_id,system_id,created_at,payload,signing_private):
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT current_key,status FROM systems WHERE system_id=?",(system_id,)).fetchone()
   if row is None or row[1]!='active':raise PermissionError('recovery system inactive')
   keys=db.execute("SELECT recipient_key FROM recovery_keys WHERE system_id=? AND key_version=?",(system_id,row[0])).fetchone()
   enc,nonce,ct=seal_snapshot(payload,load_recovery_recipient(keys[0]));manifest=canonical_recovery_manifest(snapshot_id,system_id,created_at,hashlib.sha256(ct).hexdigest());sig=sign_recovery_manifest(manifest,signing_private);db.execute("INSERT INTO snapshots VALUES(?,?,?,?,?,?,?,?,?)",(snapshot_id,system_id,created_at,row[0],enc,nonce,ct,manifest,sig))
 def plan_restore(self,system_id,target_time):
  with sqlite3.connect(self.path) as db:return [r[0] for r in db.execute("SELECT snapshot_id FROM snapshots WHERE system_id=? AND created_at<=? ORDER BY created_at DESC",(system_id,target_time)).fetchall()]
 def restore_snapshot(self,snapshot_id,system_id,recipient_private,*,now):
  with sqlite3.connect(self.path) as db:
   r=db.execute("SELECT system_id,created_at,key_version,encapsulation,nonce,ciphertext,manifest,signature FROM snapshots WHERE snapshot_id=?",(snapshot_id,)).fetchone()
   if r is None:raise KeyError(snapshot_id)
   if r[0]!=system_id:raise PermissionError('system mismatch')
   k=db.execute("SELECT signer_key FROM recovery_keys WHERE system_id=? AND key_version=?",(system_id,r[2])).fetchone()
   expected=canonical_recovery_manifest(snapshot_id,system_id,r[1],hashlib.sha256(r[5]).hexdigest())
   if k is None or expected!=r[6] or not verify_recovery_manifest(r[6],r[7],load_recovery_signer(k[0])):raise ValueError('recovery manifest invalid')
   payload=open_snapshot((r[3],r[4],r[5]),recipient_private);db.execute("INSERT INTO restores(snapshot_id,system_id,restored_at,status) VALUES(?,?,?,'verified')",(snapshot_id,system_id,now));return payload
 def compare_snapshots(self,first,second,system_id,recipient_private):
  def load(snapshot_id):
   with sqlite3.connect(self.path) as db:r=db.execute("SELECT system_id,created_at,key_version,encapsulation,nonce,ciphertext,manifest,signature FROM snapshots WHERE snapshot_id=?",(snapshot_id,)).fetchone();k=db.execute("SELECT signer_key FROM recovery_keys WHERE system_id=? AND key_version=?",(system_id,r[2])).fetchone() if r else None
   if r is None:raise KeyError(snapshot_id)
   if r[0]!=system_id or k is None:raise PermissionError('system mismatch')
   expected=canonical_recovery_manifest(snapshot_id,system_id,r[1],hashlib.sha256(r[5]).hexdigest())
   if expected!=r[6] or not verify_recovery_manifest(r[6],r[7],load_recovery_signer(k[0])):raise ValueError('recovery manifest invalid')
   return open_snapshot((r[3],r[4],r[5]),recipient_private)
  a=load(first);b=load(second);return {'equal':a==b,'first_sha256':hashlib.sha256(a).hexdigest(),'second_sha256':hashlib.sha256(b).hexdigest()}
 def restore_history(self,system_id):
  with sqlite3.connect(self.path) as db:return db.execute("SELECT snapshot_id,restored_at,status FROM restores WHERE system_id=? ORDER BY restore_id",(system_id,)).fetchall()
