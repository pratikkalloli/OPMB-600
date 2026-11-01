"""Persistent encrypted inbox with sender signature verification."""
import sqlite3
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from .crypto import canonical_message,sign_message,verify_message,seal_message,open_message,export_sender,load_sender,load_recipient
class SecureMailbox:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY,recipient_key BLOB NOT NULL,sender_key BLOB NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS messages(message_id TEXT PRIMARY KEY,sender TEXT NOT NULL,recipient TEXT NOT NULL,created_at INTEGER NOT NULL,encapsulation BLOB NOT NULL,nonce BLOB NOT NULL,ciphertext BLOB NOT NULL,signature BLOB NOT NULL)")
 def register_user(self,user_id,recipient_public,sender_public):
  if not user_id:raise ValueError('user ID required')
  raw=recipient_public.public_bytes_raw() if hasattr(recipient_public,'public_bytes_raw') else recipient_public.public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO users VALUES(?,?,?,'active')",(user_id,raw,export_sender(sender_public)))
 def deactivate_user(self,user_id):
  with sqlite3.connect(self.path) as db:return db.execute("UPDATE users SET status='inactive' WHERE user_id=? AND status='active'",(user_id,)).rowcount==1
 def send(self,message_id,sender,recipient,created_at,body,signing_private):
  with sqlite3.connect(self.path) as db:users={r[0]:r[1:] for r in db.execute("SELECT user_id,recipient_key,sender_key,status FROM users WHERE user_id IN (?,?)",(sender,recipient)).fetchall()}
  if sender not in users or recipient not in users or users[sender][2]!='active' or users[recipient][2]!='active':raise PermissionError('sender and recipient must be active')
  record=canonical_message(message_id,sender,recipient,created_at,body);sig=sign_message(record,signing_private);enc,nonce,cipher=seal_message(body,load_recipient(users[recipient][0]))
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO messages VALUES(?,?,?,?,?,?,?,?)",(message_id,sender,recipient,created_at,enc,nonce,cipher,sig))
 def receive(self,message_id,recipient,recipient_private):
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT sender,recipient,created_at,encapsulation,nonce,ciphertext,signature FROM messages WHERE message_id=?",(message_id,)).fetchone()
   if row is None:raise KeyError(message_id)
   user=db.execute("SELECT sender_key,status FROM users WHERE user_id=?",(row[0],)).fetchone();target=db.execute("SELECT status FROM users WHERE user_id=?",(recipient,)).fetchone()
  if row[1]!=recipient or target is None or target[0]!='active':raise PermissionError('message is not available to this recipient')
  if user is None or user[1]!='active':raise PermissionError('sender is not active')
  body=open_message((row[3],row[4],row[5]),recipient_private);record=canonical_message(message_id,row[0],row[1],row[2],body)
  if not verify_message(record,row[6],load_sender(user[0])):raise ValueError('message signature invalid')
  return body
