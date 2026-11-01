"""Persistent, versioned encrypted notebooks with owner access and key rotation."""
import sqlite3
from pathlib import Path
from .crypto import canonical_note,sign_note,verify_note,seal_note,open_note,export_signer,load_signer,export_owner,load_owner
class EncryptedNotebook:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS notebooks(owner TEXT PRIMARY KEY,signer_key BLOB NOT NULL,status TEXT NOT NULL,current_key INTEGER NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS owner_keys(owner TEXT NOT NULL,key_version INTEGER NOT NULL,public_key BLOB NOT NULL,PRIMARY KEY(owner,key_version))")
   db.execute("CREATE TABLE IF NOT EXISTS notes(note_id TEXT NOT NULL,owner TEXT NOT NULL,version INTEGER NOT NULL,key_version INTEGER NOT NULL,encapsulation BLOB NOT NULL,nonce BLOB NOT NULL,ciphertext BLOB NOT NULL,record BLOB NOT NULL,signature BLOB NOT NULL,PRIMARY KEY(note_id,version))")
 def create_notebook(self,owner,owner_public,signer_public):
  if not owner:raise ValueError('owner required')
  with sqlite3.connect(self.path) as db:
   db.execute("INSERT INTO notebooks VALUES(?,?,'active',1)",(owner,export_signer(signer_public)));db.execute("INSERT INTO owner_keys VALUES(?,?,?)",(owner,1,export_owner(owner_public)))
 def rotate_key(self,owner,new_public):
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT current_key,status FROM notebooks WHERE owner=?",(owner,)).fetchone()
   if row is None or row[1]!='active':raise PermissionError('notebook unavailable')
   version=row[0]+1;db.execute("INSERT INTO owner_keys VALUES(?,?,?)",(owner,version,export_owner(new_public)));db.execute("UPDATE notebooks SET current_key=? WHERE owner=?",(version,owner));return version
 def write_note(self,note_id,owner,version,text,signing_private):
  with sqlite3.connect(self.path) as db:
   nb=db.execute("SELECT signer_key,current_key,status FROM notebooks WHERE owner=?",(owner,)).fetchone()
   if nb is None or nb[2]!='active':raise PermissionError('notebook unavailable')
   previous=db.execute("SELECT MAX(version) FROM notes WHERE note_id=? AND owner=?",(note_id,owner)).fetchone()[0] or 0
   if version!=previous+1:raise ValueError('note versions must be consecutive')
   key=load_owner(db.execute("SELECT public_key FROM owner_keys WHERE owner=? AND key_version=?",(owner,nb[1])).fetchone()[0])
   enc,nonce,cipher=seal_note(text,key);record=canonical_note(note_id,owner,version,text);sig=sign_note(record,signing_private)
   if not verify_note(record,sig,load_signer(nb[0])):raise PermissionError('note signer is not the notebook authority')
   db.execute("INSERT INTO notes VALUES(?,?,?,?,?,?,?,?,?)",(note_id,owner,version,nb[1],enc,nonce,cipher,record,sig))
 def read_version(self,note_id,owner,version,owner_private):
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT key_version,encapsulation,nonce,ciphertext,record,signature FROM notes WHERE note_id=? AND owner=? AND version=?",(note_id,owner,version)).fetchone();nb=db.execute("SELECT signer_key,status FROM notebooks WHERE owner=?",(owner,)).fetchone()
  if row is None:raise KeyError('note version not found')
  if nb is None or nb[1]!='active':raise PermissionError('notebook unavailable')
  text=open_note((row[1],row[2],row[3]),owner_private)
  if not verify_note(row[4],row[5],load_signer(nb[0])):raise ValueError('note version signature invalid')
  if canonical_note(note_id,owner,version,text)!=row[4]:raise ValueError('note version integrity failure')
  return text
 def restore_version(self,note_id,owner,version,owner_private):return self.read_version(note_id,owner,version,owner_private)
 def versions(self,note_id,owner):
  with sqlite3.connect(self.path) as db:return [r[0] for r in db.execute("SELECT version FROM notes WHERE note_id=? AND owner=? ORDER BY version",(note_id,owner)).fetchall()]
