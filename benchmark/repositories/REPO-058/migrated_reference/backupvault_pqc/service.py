"""Persist authenticated backup envelopes and enforce increasing generations."""
import hashlib,sqlite3
from pathlib import Path
from .crypto import canonical_manifest,sign_manifest,verify_manifest,seal_backup,open_backup,export_signer,load_signer,load_recipient
class BackupVault:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS owners(owner TEXT PRIMARY KEY,recipient_key BLOB NOT NULL,signer_key BLOB NOT NULL,status TEXT NOT NULL,last_generation INTEGER NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS backups(backup_id TEXT PRIMARY KEY,owner TEXT NOT NULL,generation INTEGER NOT NULL,encapsulation BLOB NOT NULL,nonce BLOB NOT NULL,ciphertext BLOB NOT NULL,manifest BLOB NOT NULL,signature BLOB NOT NULL)")
 def register_owner(self,owner,recipient_public,signer_public):
  if not owner:raise ValueError('owner required')
  raw=recipient_public.public_bytes_raw() if hasattr(recipient_public,'public_bytes_raw') else recipient_public.public_bytes(__import__('cryptography').hazmat.primitives.serialization.Encoding.Raw,__import__('cryptography').hazmat.primitives.serialization.PublicFormat.Raw)
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO owners VALUES(?,?,?,'active',0)",(owner,raw,export_signer(signer_public)))
 def deactivate_owner(self,owner):
  with sqlite3.connect(self.path) as db:return db.execute("UPDATE owners SET status='inactive' WHERE owner=? AND status='active'",(owner,)).rowcount==1
 def create_backup(self,bid,owner,generation,plaintext,recipient_public,signing_private):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT status,last_generation FROM owners WHERE owner=?",(owner,)).fetchone()
  if r is None or r[0]!='active':raise PermissionError('backup owner inactive')
  if generation<=r[1]:raise ValueError('backup generation must increase')
  enc,nonce,cipher=seal_backup(plaintext,recipient_public);manifest=canonical_manifest(bid,owner,generation,hashlib.sha256(cipher).hexdigest());sig=sign_manifest(manifest,signing_private)
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO backups VALUES(?,?,?,?,?,?,?,?)",(bid,owner,generation,enc,nonce,cipher,manifest,sig));db.execute("UPDATE owners SET last_generation=? WHERE owner=?",(generation,owner))
 def restore(self,bid,owner,recipient_private):
  with sqlite3.connect(self.path) as db:
   r=db.execute("SELECT owner,generation,encapsulation,nonce,ciphertext,manifest,signature FROM backups WHERE backup_id=?",(bid,)).fetchone()
   if r is None:raise KeyError(bid)
   o=db.execute("SELECT signer_key,status FROM owners WHERE owner=?",(owner,)).fetchone()
  if r[0]!=owner or o is None or o[1]!='active':raise PermissionError('backup owner mismatch or inactive')
  if not verify_manifest(r[5],r[6],load_signer(o[0])):raise ValueError('backup manifest signature invalid')
  return open_backup((r[2],r[3],r[4]),recipient_private)
